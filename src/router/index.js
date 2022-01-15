import Vue from "vue";
import VueRouter from "vue-router";
import Search from "../views/SearchPage.vue";

Vue.use(VueRouter);

const routes = [
  {
    path: "/",
    name: "Search",
    component: Search
  },
  {
    path: "/about",
    name: "About",
    // route level code-splitting
    // this generates a separate chunk (about.[hash].js) for this route
    // which is lazy-loaded when the route is visited.
    component: () =>
      import(/* webpackChunkName: "about" */ "../views/AboutPage.vue")
  },
  {
    path: "/take-action",
    name: "Take Action",
    // route level code-splitting
    // this generates a separate chunk (about.[hash].js) for this route
    // which is lazy-loaded when the route is visited.
    component: () =>
      import(/* webpackChunkName: "about" */ "../views/TakeActionPage.vue")
  },
  {
    path: "/data-explained",
    name: "Data Explained",
    // route level code-splitting
    // this generates a separate chunk (about.[hash].js) for this route
    // which is lazy-loaded when the route is visited.
    component: () =>
      import(/* webpackChunkName: "about" */ "../views/DataExplainedPage.vue")
  },
  {
    path: "/property/:parcelNumber",
    name: "Property",
    component: () =>
      import(/* webpackChunkName: "about" */ "../views/PropertyPage.vue")
  },
  {
    path: "/explore",
    name: "Explore",
    // route level code-splitting
    // this generates a separate chunk (about.[hash].js) for this route
    // which is lazy-loaded when the route is visited.
    component: () =>
      import(/* webpackChunkName: "about" */ "../views/ExplorePage.vue")
  },
];

const router = new VueRouter({
  routes
});

export default router;
