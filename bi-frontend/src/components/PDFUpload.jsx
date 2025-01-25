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

        // Check if files are either PDFs or JPGs/JPEGs
        const invalidFiles = selectedFiles.filter(file =>
            !["application/pdf", "image/jpeg", "image/jpg"].includes(file.type)
        );

        if (invalidFiles.length > 0) {
            setError("Only PDF and JPG/JPEG files are allowed.");
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
            setError("Please select files before uploading.");
            setLoading(false);
            return;
        }

        const formData = new FormData();
        files.forEach((file) => {
            formData.append('imageData', file);
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
                        accept=".pdf,.jpg,.jpeg"
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
