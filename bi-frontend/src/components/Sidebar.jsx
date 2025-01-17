import { useState } from 'react';
import '../App.css'
import { MdClose, MdChevronRight } from "react-icons/md";
import { useDispatch } from 'react-redux';
import { clearCSV } from '../store/records';


const Sidebar = ({ csvEmpty, pdfLoaded }) => {
    const dispatch = useDispatch();
    const [open, setOpen] = useState(true);
    const handleClear = () => {
        console.log('clear');
    }
    const handleClearCSV = async () => {
        await dispatch(clearCSV());
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
                    {pdfLoaded && <button onClick={handleClear}>Clear uploaded PDF</button>}
                </div>
            </div>
            <div className={`Sidebar-toggle ${open ? 'hidden' : ''}`} onClick={() => setOpen(true)}>
                <MdChevronRight color="black" size={30} />
            </div>
        </div>
    )
}

export default Sidebar;
