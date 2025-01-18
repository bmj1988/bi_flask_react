import { createAsyncThunk, createSlice } from '@reduxjs/toolkit';
const BACKEND_SERVER_URL = process.env.REACT_APP_FLASK_URL;
// Initial state
const initialState = {
    results: [],
    match_time: 0,
    total_records: 0,
    valid_matches: 0,
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
    reducers: {
        clearResults: (state) => {
            return initialState;
        },
    },
    extraReducers: (builder) => {
        builder
            .addCase(crosscheckPDF.pending, (state) => {
                state.status = 'loading';
            })
            .addCase(crosscheckPDF.fulfilled, (state, action) => {
                console.log(action.payload);
                state.status = 'success';
                state.results = action.payload.voter_record_ocr_matches || [];
                state.match_time = action.payload.total_time || 0;
                state.total_records = action.payload.total_records || 0;
                state.valid_matches = action.payload.valid_matches || 0;
                state.total_pages = action.payload.total_pages || 0;
                state.error = null;
            })
            .addCase(crosscheckPDF.rejected, (state, action) => {
                state.status = 'failed';
                state.error = action.error.message;
            })
            .addCase(wipeUploads.fulfilled, (state) => {
                state.status = 'wipe_success';
            })
            .addCase(wipeUploads.rejected, (state, action) => {
                state.status = 'wipe_failed';
                state.error = action.error.message;
            })
            .addCase(wipeUploads.pending, (state) => {
                state.status = 'wipe_loading';
            })
    }
});
export const { clearResults } = crosscheckSlice.actions;
// Export reducer to use in the store
export default crosscheckSlice.reducer;
