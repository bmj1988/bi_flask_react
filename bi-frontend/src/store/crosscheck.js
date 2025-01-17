import { createAsyncThunk, createSlice } from '@reduxjs/toolkit';
const BACKEND_SERVER_URL = process.env.REACT_APP_FLASK_URL;
// Initial state
const initialState = {
    data: {},
    status: 'idle',
    error: null,
};

const crosscheckPDFData = async (pdf_files) => {
    const response = await fetch(`${BACKEND_SERVER_URL}/crosscheck`, {
        method: 'POST',
        body: pdf_files,
    });
    if (!response.ok) {
        throw new Error('Failed to crosscheck uploaded PDFs');
    }
    let data = await response.json();
    return data;
};

export const crosscheckPDF = createAsyncThunk('crosscheck/crosscheckPDF',
    async (pdf_files, thunkAPI) => {
        try {
            const data = await crosscheckPDFData(pdf_files);
            return data;
        } catch (error) {
            return thunkAPI.rejectWithValue(error.message);
        }
    }
);

export const wipeUploads = createAsyncThunk('crosscheck/wipeUploads',
    async (thunkAPI) => {
        try {
            let response = await fetch(`${BACKEND_SERVER_URL}/wipe_uploads`, {
                method: 'POST',
            });
            if (!response.ok) {
                throw new Error('Failed to wipe uploads');
            }
            return {};
        } catch (error) {
            return thunkAPI.rejectWithValue(error.message);
        }
    }
);

// Create the slice
const crosscheckSlice = createSlice({
    name: 'crosscheck', // Name of the slice
    initialState,
    reducers: {},
    extraReducers: (builder) => {
        builder
            .addCase(crosscheckPDF.pending, (state) => {
                state.status = 'loading';
            })
            .addCase(crosscheckPDF.fulfilled, (state, action) => {
                console.log(action.payload);
                state.status = 'success';
                state.data = action.payload;
                state.error = null;
            })
            .addCase(crosscheckPDF.rejected, (state, action) => {
                state.status = 'failed';
                state.error = action.error.message;
            })
            .addCase(wipeUploads.fulfilled, (state) => {
                state.status = 'success';
                state.data = {};
                state.error = null;
            })
            .addCase(wipeUploads.rejected, (state, action) => {
                state.status = 'failed';
                state.error = action.error.message;
            })
            .addCase(wipeUploads.pending, (state) => {
                state.status = 'loading';
            })
    }
});

// Export reducer to use in the store
export default crosscheckSlice.reducer;
