import { useDispatch } from 'react-redux';
import { loadCSV } from '../store/records';
import { useEffect, useRef, useState } from 'react';
import { MdCloudUpload } from "react-icons/md";
import "../App.css";

const CSVUpload = ({ empty, status, error: recordsError, loading, setLoading }) => {
    const dispatch = useDispatch();
    const [file, setFile] = useState(null);
    const [error, setError] = useState(recordsError);
    const fileInput = useRef(null);

    useEffect(() => {
        setError(recordsError);
    }, [recordsError]);

    // Handle file selection
    const handleFileChange = (event) => {
        const selectedFile = event.target.files[0];
        if (!selectedFile) {
            setError("No file selected.");
            return;
        }

        // Check if the file is a CSV
        if (selectedFile.type !== "text/csv") {
            setError("Only CSV files are allowed.");
            setFile(null);
            return;
        }

        setFile(selectedFile);
        setError("");
    };

    // Handle file submission (e.g., upload to backend)
    const handleSubmit = async (event) => {
        event.preventDefault();
        setLoading(true);
        if (!file) {
            setError("Please select a CSV file before uploading.");
            setLoading(false);
            return;
        }

        const formData = new FormData();
        formData.append("csv_file", file);

        try {
            await dispatch(loadCSV(formData));
            setFile(null);
            fileInput.current.value = null;
            setError(recordsError);
        } catch (error) {
            setError("Failed to upload file.");
        }
        finally {
            setLoading(false);
        }
    };

    return (
        <>
            <div className={`Upload ${empty ? "empty" : "not-empty"}`}>
                <MdCloudUpload size={100} />
                <div className="Upload-header">
                    <h3 style={{ margin: 0 }}>Upload CSV File</h3>
                    {empty ? <p>Upload a CSV of the registry you wish to crosscheck.</p>
                        : <p style={{ textWrap: "wrap", maxWidth: "400px" }}>A voter record has already been uploaded, uploading again will replace the current record.</p>
                    }
                </div>
                <form onSubmit={handleSubmit}>
                    <input
                        type="file"
                        accept=".csv"
                        onChange={handleFileChange}
                        ref={fileInput}
                        disabled={loading} />
                    <button disabled={loading} style={{ marginTop: 10 }} type="submit">Upload</button>
                </form>
            </div>
            {error && <p style={{ color: "red" }}>{error}</p>}

        </>
    )
}

export default CSVUpload;
