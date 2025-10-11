import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';
import api from '../../services/api';

// Initial state
const initialState = {
  images: [],
  currentImage: null,
  loading: false,
  uploading: false,
  uploadProgress: 0,
  error: null,
};

// Async thunks
export const fetchImages = createAsyncThunk(
  'images/fetchImages',
  async (_, { rejectWithValue }) => {
    try {
      const response = await api.get('/images/');
      return response.data;
    } catch (error) {
      return rejectWithValue(error.response?.data?.message || 'Failed to fetch images');
    }
  },
);

export const uploadImage = createAsyncThunk(
  'images/uploadImage',
  async (formData, { rejectWithValue, dispatch }) => {
    try {
      const response = await api.post('/images/', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
        onUploadProgress: (progressEvent) => {
          const percentCompleted = Math.round(
            (progressEvent.loaded * 100) / progressEvent.total,
          );
          dispatch(setUploadProgress(percentCompleted));
        },
      });
      return response.data;
    } catch (error) {
      return rejectWithValue(error.response?.data?.message || 'Failed to upload image');
    }
  },
);

export const fetchImageById = createAsyncThunk(
  'images/fetchImageById',
  async (id, { rejectWithValue }) => {
    try {
      const response = await api.get(`/images/${id}/`);
      return response.data;
    } catch (error) {
      return rejectWithValue(error.response?.data?.message || 'Failed to fetch image');
    }
  },
);

export const deleteImage = createAsyncThunk(
  'images/deleteImage',
  async (id, { rejectWithValue }) => {
    try {
      await api.delete(`/images/${id}/`);
      return id;
    } catch (error) {
      return rejectWithValue(error.response?.data?.message || 'Failed to delete image');
    }
  },
);

// Slice
const imagesSlice = createSlice({
  name: 'images',
  initialState,
  reducers: {
    clearError: (state) => {
      state.error = null;
    },
    setUploadProgress: (state, action) => {
      state.uploadProgress = action.payload;
    },
    resetUploadProgress: (state) => {
      state.uploadProgress = 0;
    },
  },
  extraReducers: (builder) => {
    builder
      // Fetch images
      .addCase(fetchImages.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(fetchImages.fulfilled, (state, action) => {
        state.loading = false;
        state.images = action.payload;
        state.error = null;
      })
      .addCase(fetchImages.rejected, (state, action) => {
        state.loading = false;
        state.error = action.payload;
      })
      // Upload image
      .addCase(uploadImage.pending, (state) => {
        state.uploading = true;
        state.error = null;
        state.uploadProgress = 0;
      })
      .addCase(uploadImage.fulfilled, (state, action) => {
        state.uploading = false;
        state.images.unshift(action.payload);
        state.error = null;
        state.uploadProgress = 100;
      })
      .addCase(uploadImage.rejected, (state, action) => {
        state.uploading = false;
        state.error = action.payload;
        state.uploadProgress = 0;
      })
      // Fetch image by ID
      .addCase(fetchImageById.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(fetchImageById.fulfilled, (state, action) => {
        state.loading = false;
        state.currentImage = action.payload;
        state.error = null;
      })
      .addCase(fetchImageById.rejected, (state, action) => {
        state.loading = false;
        state.error = action.payload;
      })
      // Delete image
      .addCase(deleteImage.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(deleteImage.fulfilled, (state, action) => {
        state.loading = false;
        state.images = state.images.filter((img) => img.id !== action.payload);
        state.error = null;
      })
      .addCase(deleteImage.rejected, (state, action) => {
        state.loading = false;
        state.error = action.payload;
      });
  },
});

// Actions
export const { clearError, setUploadProgress, resetUploadProgress } = imagesSlice.actions;

// Selectors
export const selectImages = (state) => state.images.images;
export const selectCurrentImage = (state) => state.images.currentImage;
export const selectImagesLoading = (state) => state.images.loading;
export const selectUploading = (state) => state.images.uploading;
export const selectUploadProgress = (state) => state.images.uploadProgress;
export const selectImagesError = (state) => state.images.error;

// Reducer
export default imagesSlice.reducer;
