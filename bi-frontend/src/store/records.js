import { createAsyncThunk, createSlice } from '@reduxjs/toolkit';

const BACKEND_SERVER_URL = process.env.REACT_APP_FLASK_URL;
// Initial state
const initialState = {
    empty: true,
    pdfLoaded: false,
    error: null,
    status: 'idle',
};

const loadRecordsData = async (csv) => {
    const response = await fetch(`${BACKEND_SERVER_URL}/upload_csv`, {
        method: 'POST',
        body: csv,
    });
    if (!response.ok) {
        throw new Error('Failed to upload CSV');
    }
    return response.json();
};

export const loadCSV = createAsyncThunk('records/loadCSV',
    async (csv, thunkAPI) => {
        try {
            const data = await loadRecordsData(csv);
            return data;
        } catch (error) {
            return thunkAPI.rejectWithValue(error.message);
        }
    }
);

export const splash = createAsyncThunk('records/splash',
    async (thunkAPI) => {
        try {
            const response = await fetch(`${BACKEND_SERVER_URL}/splash`, {
                method: 'GET',
            });
            if (!response.ok) throw new Error('Failed to get records status');
            const data = await response.json();
            return data
        } catch (error) {
            return thunkAPI.rejectWithValue(error.message);
        }
    }
);

export const clearCSV = createAsyncThunk('records/clearCSV',
    async (thunkAPI) => {
        try {
            const response = await fetch(`${BACKEND_SERVER_URL}/clear_csv`, {
                method: 'POST',
            });
            if (!response.ok) throw new Error('Failed to clear CSV');
        } catch (error) {
            return thunkAPI.rejectWithValue(error.message);
        }
    }
);


// Create the slice
const recordsSlice = createSlice({
    name: 'records', // Name of the slice
    initialState,
    reducers: {
        setPdfEmpty: (state) => {
            state.pdfLoaded = false;
        },
    },
    extraReducers: (builder) => {
        builder
            .addCase(loadCSV.pending, (state) => {
                state.status = 'loading';
            })
            .addCase(loadCSV.fulfilled, (state) => {
                state.status = 'succeeded';
                state.empty = false;
            })
            .addCase(loadCSV.rejected, (state, action) => {
                state.status = 'failed';
                state.error = action.error.message;
            })
            .addCase(splash.fulfilled, (state, action) => {
                console.log(action.payload)
                state.empty = action.payload.dataframeEmpty;
                state.pdfLoaded = action.payload.pdfLoaded;
            })
            .addCase(splash.rejected, (state, action) => {
                state.status = 'failed';
                state.error = action.error.message;
            })
            .addCase(clearCSV.fulfilled, (state) => {
                state.status = 'succeeded';
                state.empty = true;
            })
            .addCase(clearCSV.rejected, (state, action) => {
                state.status = 'failed';
                state.error = action.error.message;
            })
    }
});

export const { setPdfEmpty } = recordsSlice.actions;

// Export reducer to use in the store
export default recordsSlice.reducer;
