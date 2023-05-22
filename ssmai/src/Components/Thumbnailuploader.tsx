import React, { useState } from 'react';
import '../Styles/Thumbnailuploader.css';

const ThumbnailUploader = () => {
  const [thumbnails, setThumbnails] = useState<string[]>([]);

  const handleUpload = (event: React.ChangeEvent<HTMLInputElement>) => {
    const files = event.target.files;
    if (files) {
      const fileArray = Array.from(files);
      const thumbnailPromises = fileArray.map((file) => {
        return new Promise<string>((resolve, reject) => {
          const reader = new FileReader();
          reader.onload = () => {
            const imageDataUrl = reader.result as string;
            resolve(imageDataUrl);
          };
          reader.onerror = reject;
          reader.readAsDataURL(file);
        });
      });

      Promise.all(thumbnailPromises)
        .then((thumbnailUrls) => {
          setThumbnails(thumbnailUrls);
        })
        .catch((error) => {
          console.error('Error reading image file:', error);
        });
    }
  };

  return (
    <div className="thumbnail-uploader">
      <h2>Thumbnail Uploader</h2>
      <input type="file" multiple onChange={handleUpload} accept="image/*" />
      <div className="thumbnails">
        {thumbnails.map((url) => (
          <div
            className="thumbnail"
            style={{ backgroundImage: 'url("${url}")' }}
            key={url}
          />
        ))}
      </div>
    </div>
  );
};

export default ThumbnailUploader;