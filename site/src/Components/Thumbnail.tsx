import React from 'react';
import '../Styles/Thumbnail.css';

interface ThumbnailProps {
  file: File;
}

const Thumbnail: React.FC<ThumbnailProps> = ({ file }) => {
  const reader = new FileReader();
  reader.readAsDataURL(file);

  return (
    <div className="thumbnail">
      <img src={URL.createObjectURL(file)} alt="Thumbnail" />
    </div>
  );
};

export default Thumbnail;