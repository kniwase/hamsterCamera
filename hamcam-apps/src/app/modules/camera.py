from fastapi import WebSocket
from starlette.websockets import WebSocketDisconnect
import asyncio
import msgpack
import datauri
import uuid
import logging
import traceback

logging.basicConfig(level=logging.INFO)


class Camera():
    def __init__(self):
        self._ws_connected = False
        self._request_queue = None
        self._waiting_tasks = {}

    async def get_photo(self):
        res = await self._execute_rpc_task("getPhoto")
        return {
            "img": datauri.DataURI(res["photo"]),
            "datetime": res["datetime"]
        }

    async def get_battery_status(self):
        return await self._execute_rpc_task("getBatteryStatus")

    async def create_connection(self, websocket: WebSocket):
        await websocket.accept()
        if self._ws_connected:
            await self._reject_connection(websocket)
        else:
            await self._main(websocket)

    async def _main(self, websocket: WebSocket):
        try:
            loop = asyncio.get_running_loop()
            self._request_queue = asyncio.Queue(loop=loop)
            self._ws_connected = True
            logging.info("Camera Connected")
            await asyncio.gather(
                self._response_reciever(websocket),
                self._request_sender(websocket),
                loop=loop
            )
        except WebSocketDisconnect:
            logging.warning("Camera Disconnected")
        except Exception:
            logging.error(traceback.format_exc())
        finally:
            await websocket.close()
            self.__init__()

    async def _reject_connection(self, websocket: WebSocket):
        try:
            await websocket.close()
        except WebSocketDisconnect:
            logging.warning("Camera Error: New Connection Rejected")
            return

    async def _request_sender(self, websocket):
        while self._ws_connected:
            try:
                req = await self._request_queue.get()
                req_bytes = msgpack.packb(req)
                await websocket.send_bytes(req_bytes)
            except WebSocketDisconnect:
                raise
            except Exception:
                logging.error("Camera Error: Sending Request")
                logging.error(traceback.format_exc())

    async def _response_reciever(self, websocket):
        while self._ws_connected:
            try:
                res_bytes = await websocket.receive_bytes()
                res_data = msgpack.unpackb(res_bytes)
                callback = self._waiting_tasks.get(res_data["id"])
                if callback:
                    await callback(res_data)
                else:
                    logging.warning("Camera Warning: ReqID not found")
            except WebSocketDisconnect:
                raise
            except Exception:
                logging.error("Camera Error: Recieving Response")
                logging.error(traceback.format_exc())

    async def _execute_rpc_task(self, method, params=None):
        if not self._ws_connected:
            raise Exception("Camera Error: Not Connected")
        req_id = uuid.uuid4().hex
        queue = asyncio.Queue()
        self._waiting_tasks[req_id] = queue.put
        req = {"id": req_id, "method": method, "params": params}
        await self._request_queue.put(req)
        try:
            res = await asyncio.wait_for(queue.get(), timeout=30.0)
        except asyncio.TimeoutError as err:
            logging.error("Camera Error: Request Timeout")
            raise err
        error = res.get("error")
        if error:
            datail = error.get("detail")
            if datail:
                err_msg = "\n".join((
                    datail.get("name", ""),
                    datail.get("message", ""),
                    datail.get("stack", "")
                ))
            else:
                err_msg = f"{error['message']}"
            raise Exception(f"Camera Error: {err_msg}")
        ret = res.get("result")
        if ret is None:
            raise Exception("Camera Error: Invalid Response")
        return ret


camera = Camera()
