import { useDispatch } from 'react-redux';
import { crosscheckPDF } from '../store/crosscheck';
import { useEffect, useRef, useState } from 'react';
import { MdCloudUpload } from "react-icons/md";
import "../App.css";

const PDFUpload = ({ crosscheckError, crosscheckStatus, loading, setLoading }) => {
    const dispatch = useDispatch();
    const [files, setFiles] = useState([]);
    const [error, setError] = useState("");
    const fileInput = useRef(null);

    useEffect(() => {
        setError(crosscheckError);
    }, [crosscheckError]);

    // Handle file selection
    const handleFileChange = (event) => {
        const selectedFiles = Array.from(event.target.files);

        // Check if all selected files are PDFs
        const invalidFiles = selectedFiles.filter(file => file.type !== "application/pdf");

        if (invalidFiles.length > 0) {
            setError("Only PDF files are allowed.");
            return;
        }

        setFiles(selectedFiles);
        setError("");
    };

    // Handle file submission (e.g., upload to backend)
    const handleSubmit = async (event) => {
        event.preventDefault();
        setLoading(true);
        if (!files.length) {
            setError("Please select a PDF file before uploading.");
            setLoading(false);
            return;
        }

        const formData = new FormData();
        files.forEach((file, index) => {
            formData.append(`pdf_files`, file);
        });

        try {
            await dispatch(crosscheckPDF(formData));
            setFiles([]);
            fileInput.current.value = null;
            setError("");
        } catch (error) {
            setError("Failed to upload files.");
        }
        finally {
            setLoading(false);
        }
    };

    return (
        <>
            <div className={`Upload`}>
                <MdCloudUpload size={100} />
                <div className="Upload-header">
                    <h3 style={{ margin: 0 }}>Upload PDF Files</h3>
                    <p>Upload PDF files of signed petitions to crosscheck.</p>
                </div>
                <form onSubmit={handleSubmit}>
                    <input
                        type="file"
                        accept=".pdf"
                        onChange={handleFileChange}
                        multiple
                        disabled={loading}
                        ref={fileInput} />
                    <button disabled={loading} style={{ marginTop: 10 }} type="submit">Upload</button>
                </form>
            </div>
            {error && <p style={{ color: "red" }}>{error}</p>}
        </>
    )
}

export default PDFUpload;
