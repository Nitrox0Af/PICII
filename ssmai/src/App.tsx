import './Styles/Global.css';
import './Styles/Styles.css';
import React from 'react'
import ThumbnailUploader from './Components/Thumbnailuploader';
function App() {
  return (
    <div className='infos'>
      <h1 className='Uploader'>
        <ThumbnailUploader />
      </h1>
      <h1 className='n1'>
        CPF*:
      </h1>
      <h1 className='n2'>
        Nome*:
      </h1>
      <h1 className='n3'>
        Apelido*:
      </h1>
      <h1 className='n4'>
        Parentesco*:
      </h1>
      <input className='cpf' placeholder='000.000.000-00'></input>
      <input className='name' placeholder='fulano'></input>
      <input className='surname' placeholder='ciclano'></input>
      <input className='relationship' placeholder='primo'></input>
   </div>
  );
}

export default App;
