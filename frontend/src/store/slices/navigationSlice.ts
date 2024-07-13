import { createSlice } from "@reduxjs/toolkit";

interface NavigationState {
  currentScreen: string;
}

const initialState: NavigationState = {
  currentScreen: "/",
};

const navigationSlice = createSlice({
  name: "navigation",
  initialState,
  reducers: {
    setCurrentScreen(state, action) {
      state.currentScreen = action.payload;
    },
  },
});

export const { setCurrentScreen } = navigationSlice.actions;

export default navigationSlice.reducer;
