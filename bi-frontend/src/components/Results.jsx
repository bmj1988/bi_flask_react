import React from "react";

const ResultsTable = ({ results }) => {
  return (
    <div>
      <h2>Results Table</h2>
      <table border="1">
        <thead>
          <tr>
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
                <td>{result.OCR_RECORD}</td>
                <td>{result.MATCHED_RECORD}</td>
                <td>{result.SCORE}</td>
                <td>{result.VALID ? "✔️ Yes" : "❌ No"}</td>
              </tr>
            ))
          ) : (
            <tr>
              <td colSpan="4" style={{ textAlign: "center" }}>
                No results available
              </td>
            </tr>
          )}
        </tbody>
      </table>
    </div>
  );
};

export default ResultsTable;
