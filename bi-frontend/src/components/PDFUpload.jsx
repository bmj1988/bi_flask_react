import { useDispatch } from 'react-redux';
import { crosscheckPDF } from '../store/crosscheck';
import { useEffect, useRef, useState } from 'react';
import { MdCloudUpload } from "react-icons/md";


const PDFUpload = ({ crosscheckError, crosscheckStatus }) => {
    const dispatch = useDispatch();
    const [files, setFiles] = useState([]);
    const [error, setError] = useState("");
    const [loading, setLoading] = useState(false);
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
        if (!files) {
            setError("Please select a PDF file before uploading.");
            return;
        }

        const formData = new FormData();
        files.forEach((file, index) => {
            formData.append(`pdf_files`, file);
        });

        try {
            await dispatch(crosscheckPDF(formData));
            alert("File uploaded successfully!");
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
                    ref={fileInput} />
                <button style={{ marginTop: 10 }} type="submit">Upload</button>
            </form>
            {error && <p style={{ color: "red" }}>{error}</p>}
        </div>
    )
}

export default PDFUpload;
