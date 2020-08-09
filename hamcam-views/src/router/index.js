import Vue from "vue";
import VueRouter from "vue-router";

Vue.use(VueRouter);
const routes = [
  {
    path: "/camera",
    name: "Camera",
    component: () => import("../views/Camera.vue"),
  },
  {
    path: "*",
    name: "NotMatchPageName",
    component: () => import("../views/NotFound.vue"),
    alias: ``,
  },
];

const router = new VueRouter({
  mode: "history",
  base: process.env.BASE_URL,
  routes,
});

export default router;
