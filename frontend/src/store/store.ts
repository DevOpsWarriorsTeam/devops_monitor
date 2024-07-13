import { configureStore } from "@reduxjs/toolkit";
import containerSlice from "./slices/containerSlice";
import navigationSlice from "./slices/navigationSlice";
import logSlice from "./slices/logSlice";

const store = configureStore({
  reducer: {
    container: containerSlice,
    navigation: navigationSlice,
    log: logSlice,
  },
  middleware: (getDefaultMiddleware) =>
    getDefaultMiddleware({
      serializableCheck: false,
    }),
});

export default store;

export type RootState = ReturnType<typeof store.getState>;

export type AppDispatch = typeof store.dispatch;
