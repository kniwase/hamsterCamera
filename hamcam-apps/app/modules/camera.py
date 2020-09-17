from fastapi import WebSocket
from starlette.websockets import WebSocketDisconnect
import asyncio
from queue import (Queue, Empty)
import datauri
import uuid
import logging
import traceback

logging.basicConfig(level=logging.INFO)


class Camera():
    def __init__(self):
        self._loop = None
        self._ws_connected = False
        self._request_queue = None
        self._waiting_tasks = {}

    def get_photo(self):
        res = self._execute_rpc_task("getPhoto")
        return {
            "img": datauri.DataURI(res["photo"]),
            "datetime": res["datetime"]
        }

    async def create_connection(self, websocket: WebSocket):
        await websocket.accept()
        if self._ws_connected:
            await self._reject_connection(websocket)
        else:
            await self._main(websocket)

    async def _main(self, websocket: WebSocket):
        try:
            self._loop = asyncio.get_running_loop()
            self._request_queue = Queue()
            self._ws_connected = True
            logging.info("Camera Connected")
            await asyncio.gather(
                self._response_reciever(websocket),
                self._request_sender(websocket),
                loop=self._loop
            )
        except WebSocketDisconnect:
            logging.warning("Camera Disconnected")
        except Exception:
            logging.error(traceback.format_exc())
        finally:
            self.__init__()
            await websocket.close()

    async def _reject_connection(self, websocket: WebSocket):
        try:
            await websocket.close()
        except WebSocketDisconnect:
            logging.warning("Camera Error: New Connection Rejected")
            return

    async def _request_sender(self, websocket):
        while self._ws_connected:
            try:
                req = await self._loop.run_in_executor(
                    None, self._request_queue.get)
                await websocket.send_json(req)
            except WebSocketDisconnect:
                raise
            except Exception:
                logging.error("Camera Error: Sending Request")
                logging.error(traceback.format_exc())

    async def _response_reciever(self, websocket):
        while self._ws_connected:
            try:
                res_data = await websocket.receive_json()
                callback = await self._loop.run_in_executor(
                    None, self._waiting_tasks.get, res_data["id"])
                if callback:
                    await self._loop.run_in_executor(None, callback, res_data)
                else:
                    logging.warning("Camera Warning: ReqID not found")
            except WebSocketDisconnect:
                raise
            except Exception:
                logging.error("Camera Error: Recieving Response")
                logging.error(traceback.format_exc())

    def _execute_rpc_task(self, method, params=[]):
        if not self._ws_connected:
            raise Exception("Camera Error: Not Connected")
        req_id = uuid.uuid4().hex
        queue = Queue()
        self._waiting_tasks[req_id] = queue.put
        req = {"method": method,
               "params": params,
               "id": req_id,
               "jsonrpc": "2.0"}
        self._request_queue.put(req)
        try:
            res = queue.get(timeout=30)
        except Empty as err:
            logging.error("Camera Error: Request Timeout")
            raise err
        finally:
            self._waiting_tasks.pop(req_id)
        error = res.get("error")
        if error:
            raise Exception(f"Camera Error: {error['message']}")
        ret = res.get("result")
        if ret is None:
            raise Exception("Camera Error: Invalid Response")
        return ret


camera = Camera()
