import React from "react";
import { useDispatch, useSelector } from "react-redux";
import { clearResults, wipeUploads } from "../store/crosscheck";
import "../App.css";

const ResultsTable = () => {
  const { results, match_time, total_records, valid_matches, total_pages } = useSelector(state => state.crosscheck);
  const dispatch = useDispatch();
  const handleClearResults = async () => {
    await dispatch(clearResults());
    await dispatch(wipeUploads())
  }
  return (
    <div className="results-container">
      <h2>Results Table</h2> <button onClick={handleClearResults}>Clear Results</button>
      <p>{`${total_records} records scanned on ${total_pages} pages in ${match_time.toFixed(2)} seconds`}</p>
      <p>{`${valid_matches} valid matches found - ${((valid_matches / total_records) * 100).toFixed(2)}% valid match rate`}</p>
      <div className="table-wrapper">
        <table className="results-table">
          <thead>
            <tr>
              <th>Page</th>
              <th>Row</th>
              <th>OCR Record</th>
              <th>Matched Record</th>
              <th>Score</th>
              <th>Valid</th>
            </tr>
          </thead>
          <tbody>
            {results.length > 0 ? (
              results.map((result, index) => (
                <tr key={index}>
                  <td>{result.PAGE}</td>
                  <td>{result.ROW}</td>
                  <td>{result.OCR_RECORD}</td>
                  <td>{result.MATCHED_RECORD}</td>
                  <td>{result.SCORE}</td>
                  <td>{result.VALID ? "✔️ Yes" : "❌ No"}</td>
                </tr>
              ))
            ) : (
              <tr>
                <td colSpan="6" style={{ textAlign: "center" }}>
                  No results available
                </td>
              </tr>
            )}
          </tbody>
        </table>
      </div>
    </div>
  );
};

export default ResultsTable;
