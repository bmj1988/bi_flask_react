import './App.css';
import { useDispatch, useSelector } from 'react-redux'
import { splash } from './store/records';
import { useEffect, useState } from 'react';
import Sidebar from './components/Sidebar';
import CSVUpload from './components/CSVUpload';
import PDFUpload from './components/PDFUpload';

const App = () => {
  const dispatch = useDispatch();
  const { empty, error: recordsError, status: recordsStatus } = useSelector(state => state.records);
  const { data, error: crosscheckError, status: crosscheckStatus } = useSelector(state => state.crosscheck);

  useEffect(() => {
    dispatch(splash());
  }, [dispatch]);

  return (
    <div className="App">
      <div className="Main">
        <Sidebar csvEmpty={empty} pdfLoaded={Object.entries(data).length > 0 ? true : false} />
        <div className="Main-content">
          <CSVUpload empty={empty} error={recordsError} status={recordsStatus} />
          <PDFUpload crosscheckError={crosscheckError} crosscheckStatus={crosscheckStatus} />
        </div>
      </div>
    </div>
  );
}

export default App;
