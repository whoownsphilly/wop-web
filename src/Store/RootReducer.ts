import { combineReducers } from "redux";

// Home Imports
import { HomeState } from "../Components/Home/types";
import HomeReducer from "../Components/Home/redux/reducer";
import { Actions as HomeActions } from "../Components/Home/redux/actions";

// Property Imports
import { PropertyState } from "../Components/Properties/types";
import PropertyReducer from "../Components/Properties/redux/reducer";
import { Actions as PropertyActions } from "../Components/Properties/redux/actions";

export type RootActionTypes = HomeActions | PropertyActions;

export interface RootState {
  home: HomeState;
  properties: PropertyState;
}

export const RootReducer = combineReducers({
  home: HomeReducer,
  properties: PropertyReducer,
});
