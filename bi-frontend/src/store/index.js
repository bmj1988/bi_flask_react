import { configureStore } from '@reduxjs/toolkit';
import recordReducer from './records';
import crosscheckSlice from './crosscheck';

const store = configureStore({
  reducer: {
    records: recordReducer,
    crosscheck: crosscheckSlice,
  },
});

export default store;
