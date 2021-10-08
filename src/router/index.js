import Vue from "vue";
import VueRouter from "vue-router";
import Home from "../views/Home.vue";

Vue.use(VueRouter);

const routes = [
  {
    path: "/",
    name: "Home",
    component: Home
  },
  {
    path: "/about",
    name: "About",
    // route level code-splitting
    // this generates a separate chunk (about.[hash].js) for this route
    // which is lazy-loaded when the route is visited.
    component: () =>
      import(/* webpackChunkName: "about" */ "../views/About.vue")
  },
  {
    path: "/take-action",
    name: "Take Action",
    // route level code-splitting
    // this generates a separate chunk (about.[hash].js) for this route
    // which is lazy-loaded when the route is visited.
    component: () =>
      import(/* webpackChunkName: "about" */ "../views/TakeAction.vue")
  },
  {
    path: "/data-explained",
    name: "Data Explained",
    // route level code-splitting
    // this generates a separate chunk (about.[hash].js) for this route
    // which is lazy-loaded when the route is visited.
    component: () =>
      import(/* webpackChunkName: "about" */ "../views/DataExplained.vue")
  },
  {
    path: "/property/:parcelNumber",
    name: "Property",
    component: () =>
      import(/* webpackChunkName: "about" */ "../views/Property.vue")
  },
  {
    path: "/owner/:ownerName",
    name: "Owner",
    component: () =>
      import(/* webpackChunkName: "about" */ "../views/Owner.vue")
  },
  {
    path: "/mailing_address/:fullMailingAddress",
    name: "Mailing Address",
    component: () =>
      import(/* webpackChunkName: "about" */ "../views/MailingAddress.vue")
  }
];

const router = new VueRouter({
  routes
});

export default router;
