import './Styles/Global.css';
import './Styles/Styles.css';
import React from 'react'
import InputsData from './Components/InputsData';
import UploadForm from './Components/UploadForm';

function App() {
  return (
    <div className='infos'>
      <h1>
        Upload das fotos
      </h1>
      <UploadForm maxFileSizeKB={128} maxNumFiles={5} />
      <h1 className='n1'>
        CPF*:
      </h1>
      <h1 className='n2'>
        Nome*:
      </h1>
      <h1 className='n3'>
        Apelido:
      </h1>
      <h1 className='n4'>
        Parentesco:
      </h1>
      <InputsData/>
   </div>
  );
}

export default App;
