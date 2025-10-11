import { configureStore } from '@reduxjs/toolkit';
import authReducer from './slices/authSlice';
import imagesReducer from './slices/imagesSlice';

export const store = configureStore({
  reducer: {
    auth: authReducer,
    images: imagesReducer,
  },
  middleware: (getDefaultMiddleware) => getDefaultMiddleware({
    serializableCheck: {
      // Ignore these action types
      ignoredActions: ['images/uploadImage/pending'],
      // Ignore these field paths in all actions
      ignoredActionPaths: ['payload.file'],
      // Ignore these paths in the state
      ignoredPaths: ['images.uploadProgress'],
    },
  }),
  devTools: process.env.NODE_ENV !== 'production',
});

// Export types for TypeScript (if needed)
export const selectAuth = (state) => state.auth;
export const selectImages = (state) => state.images;
