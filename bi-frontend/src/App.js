import './App.css';
import { useDispatch, useSelector } from 'react-redux'
import { splash } from './store/records';
import { useEffect, useState } from 'react';
import Sidebar from './components/Sidebar';
import CSVUpload from './components/CSVUpload';
import PDFUpload from './components/PDFUpload';
import ResultsTable from './components/Results';
import LoadingModal from './components/LoadingModal';

const App = () => {
  const dispatch = useDispatch();
  const { empty, pdfLoaded, error: recordsError, status: recordsStatus } = useSelector(state => state.records);
  const { results, error: crosscheckError, status: crosscheckStatus } = useSelector(state => state.crosscheck);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    dispatch(splash());
  }, [dispatch]);

  return (
    <div className="App">
      <div className="Main">
        <Sidebar csvEmpty={empty} pdfLoaded={(pdfLoaded || crosscheckStatus === 'success') ? true : false} />
        <div className="Main-content">
          <CSVUpload empty={empty} error={recordsError} status={recordsStatus} loading={loading} setLoading={setLoading}/>
          <PDFUpload crosscheckError={crosscheckError} crosscheckStatus={crosscheckStatus} loading={loading} setLoading={setLoading}/>
          {(crosscheckStatus === 'success' || crosscheckStatus.startsWith('wipe_')) && results.length > 0 && <ResultsTable />}
        </div>
      </div>
      <LoadingModal loading={loading} />
    </div>
  );
}

export default App;
