import Vue from "vue";
import VueRouter from "vue-router";
import Search from "../views/SearchPage.vue";

Vue.use(VueRouter);

const routes = [
  {
    path: "/",
    name: "Search",
    component: Search,
  },
  {
    path: "/about",
    name: "About",
    // route level code-splitting
    // this generates a separate chunk (about.[hash].js) for this route
    // which is lazy-loaded when the route is visited.
    component: () =>
      import(/* webpackChunkName: "about" */ "../views/AboutPage.vue"),
  },
  {
    path: "/take-action",
    name: "Take Action",
    // route level code-splitting
    // this generates a separate chunk (about.[hash].js) for this route
    // which is lazy-loaded when the route is visited.
    component: () =>
      import(/* webpackChunkName: "about" */ "../views/TakeActionPage.vue"),
  },
  {
    path: "/property/:parcelNumber",
    name: "Property",
    component: () =>
      import(
        /* webpackChunkName: "property-page" */ "../views/PropertyPage.vue"
      ),
    children: [
      {
        path: "",
        redirect: "property-summary",
      },
      {
        path: "property-summary",
        props: (route) => ({ parcelNumber: route.params.parcelNumber }),
        name: "property-summary",
        component: () =>
          import(
            /* webpackChunkName: "property-summary" */ "../components/page/property/index.vue"
          ),
      },
      {
        path: "owner",
        name: "owner",
        props: (route) => ({ parcelNumber: route.params.parcelNumber }),
        component: () =>
          import(
            /* webpackChunkName: "owner" */ "../components/page/owner/index.vue"
          ),
      },
      {
        path: "property-details",
        name: "property-details",
        props: (route) => ({ parcelNumber: route.params.parcelNumber }),
        component: () =>
          import(
            /* webpackChunkName: "property-details" */ "../components/page/property/PropertyDetails.vue"
          ),
      },
      {
        path: "crowd-sourced",
        name: "crowd-sourced",
        props: (route) => ({ parcelNumber: route.params.parcelNumber }),
        component: () =>
          import(
            /* webpackChunkName: "property-details" */ "../components/page/crowdSourced/index.vue"
          ),
      },
    ],
  },
  {
    path: "/explore",
    name: "Explore",
    // route level code-splitting
    // this generates a separate chunk (about.[hash].js) for this route
    // which is lazy-loaded when the route is visited.
    component: () =>
      import(/* webpackChunkName: "about" */ "../views/ExplorePage.vue"),
  },
  {
    path: "/neighborhoods",
    name: "Neighborhoods",
    // route level code-splitting
    // this generates a separate chunk (about.[hash].js) for this route
    // which is lazy-loaded when the route is visited.
    component: () =>
      import(/* webpackChunkName: "about" */ "../views/NeighborhoodsPage.vue"),
  },
  {
    path: "/neighborhood-view",
    name: "NeighborhoodView",
    component: () =>
      import(
        /* webpackChunkName: "about" */ "../views/NeighborhoodListViewPage.vue"
      ),
  },
];

const router = new VueRouter({
  routes,
});

export default router;
