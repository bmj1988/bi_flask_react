import './App.css';
import { useDispatch, useSelector } from 'react-redux'
import { splash } from './store/records';
import { useEffect, useState } from 'react';
import Sidebar from './components/Sidebar';
import CSVUpload from './components/CSVUpload';
import PDFUpload from './components/PDFUpload';
import ResultsTable from './components/Results';
const App = () => {
  const dispatch = useDispatch();
  const { empty, error: recordsError, status: recordsStatus } = useSelector(state => state.records);
  const { data, error: crosscheckError, status: crosscheckStatus } = useSelector(state => state.crosscheck);
  const [results, setResults] = useState([])

  useEffect(() => {
    if (data.voter_record_ocr_matches) {
      setResults(data.voter_record_ocr_matches)
    }
  }, [data])

  console.log(data)

  useEffect(() => {
    dispatch(splash());
  }, [dispatch]);

  return (
    <div className="App">
      <div className="Main">
        <Sidebar csvEmpty={empty} pdfLoaded={crosscheckStatus === 'success' ? true : false} />
        <div className="Main-content">
          <CSVUpload empty={empty} error={recordsError} status={recordsStatus} />
          <PDFUpload crosscheckError={crosscheckError} crosscheckStatus={crosscheckStatus} />
          {crosscheckStatus === 'success' && <ResultsTable results={results} />}
        </div>
      </div>
    </div>
  );
}

export default App;
