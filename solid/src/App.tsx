import type { Component } from 'solid-js';
import Header from "./components/Header"
import Home from "./routes/Home";
import { useRoutes} from "@solidjs/router";
import { lazy } from "solid-js";

const routes = [
    {
        path: "/",
        component: Home
    },
    {
        path: "/about",
        component: lazy(() => import("./routes/About")),
    },
    {
        path: "/take-action",
        component: lazy(() => import("./routes/TakeAction")),
    },
    {
        path: "/neighborhoods",
        component: lazy(() => import("./routes/Neighborhoods")),
    },
    {
        path: "/properties/:id",
        children: [
            { path: "/", component: lazy(() => import("./routes/properties/Summary")), },
            { path: "/details", component: lazy(() => import("./routes/properties/Summary")), },
            { path: "/owner", component: lazy(() => import("./routes/properties/Summary")) },
            { path: "/crowd", component: lazy(() => import("./routes/properties/Summary")) },
        ]
    },
];

const App: Component = () => {
const Routes = useRoutes(routes);
  return (
      <>
      <Header/>
      <Routes />
      </>
)}

export default App;
