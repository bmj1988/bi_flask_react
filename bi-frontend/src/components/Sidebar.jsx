import { useState } from 'react';
import '../App.css'
import { MdClose, MdChevronRight } from "react-icons/md";
import { useDispatch } from 'react-redux';
import { clearCSV, setPdfEmpty } from '../store/records';
import { wipeUploads } from '../store/crosscheck';

const Sidebar = ({ csvEmpty, pdfLoaded }) => {
    const dispatch = useDispatch();
    const [open, setOpen] = useState(true);

    const handleClearCSV = async () => {
        await dispatch(clearCSV());
    }
    const handleClearTempFiles= async () => {
        await dispatch(wipeUploads());
        await dispatch(setPdfEmpty());
    }


    return (
        <div className="Sidebar-container">
            <div className={`Sidebar ${!open ? 'hidden' : ''}`}>
                <header className="Sidebar-header">
                    <MdClose color="black" size={20} style={{cursor: 'pointer'}} onClick={() => setOpen(false)} />
                </header>
                <div className="Sidebar-content">
                    <h2>Ballot Initiative Project</h2>
                    {!csvEmpty && <button onClick={handleClearCSV}>Clear uploaded CSV</button>}
                    {pdfLoaded && <button onClick={handleClearTempFiles}>Clear uploaded PDF</button>}
                </div>
            </div>
            <div className={`Sidebar-toggle ${open ? 'hidden' : ''}`} onClick={() => setOpen(true)}>
                <MdChevronRight color="black" size={30} />
            </div>
        </div>
    )
}

export default Sidebar;
