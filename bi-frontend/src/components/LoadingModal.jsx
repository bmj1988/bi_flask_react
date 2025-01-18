import React from "react";
import { RingLoader } from "react-spinners"; // Import spinner
import "../App.css"; // Import styles

const LoadingModal = ({ loading }) => {
  if (!loading) return null; // Don't render the modal if loading is false

  return (
    <div className="modal-overlay">
        <RingLoader size={100} color="#1a63ac" />
    </div>
  );
};

export default LoadingModal;
