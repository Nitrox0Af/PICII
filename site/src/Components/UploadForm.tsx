import React, { useState } from 'react';
import '../Styles/UploadForm.css';
import Thumbnail from './Thumbnail';

interface UploadFormProps {
  maxFileSizeKB: number;
  maxNumFiles: number;
}

const UploadForm: React.FC<UploadFormProps> = ({ maxFileSizeKB, maxNumFiles }) => {
  const [selectedFiles, setSelectedFiles] = useState<File[]>([]);

  const handleFileChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    const files = Array.from(event.target.files || []);
    setSelectedFiles(files.slice(0, maxNumFiles));
  };

  return (
    <div className="upload-form">
      <input type="file" multiple onChange={handleFileChange} />
      <div className="thumbnail-container">
        {selectedFiles.map((file, index) => (
          <Thumbnail key={index} file={file} />
        ))}
      </div>
    </div>
  );
};

export default UploadForm;