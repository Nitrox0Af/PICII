import React, { useState, ChangeEvent, FormEvent } from 'react';

const App = () => {
  const [var1, setVar1] = useState('');
  const [var2, setVar2] = useState('');
  const [resultado, setResultado] = useState('');
  const [str1, setStr1] = useState('');
  const [str2, setStr2] = useState('');
  const [str3, setStr3] = useState('');
  const [str4, setStr4] = useState('');
  const [photoFiles, setPhotoFiles] = useState<File[]>([]);

  const handleInputChange = (event: ChangeEvent<HTMLInputElement>, setValue: React.Dispatch<React.SetStateAction<string>>) => {
    const { value } = event.target;
    setValue(value);
  };

  const handleFormSubmit = async (event: FormEvent<HTMLFormElement>): Promise<void> => {
    event.preventDefault();

    const response = await fetch('http://localhost:8000/api/somar/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ var_1: var1, var_2: var2 }),
    });

    const data = await response.json();
    setResultado(data.resultado);
  };

  const handleStringsSubmit = async (event: FormEvent<HTMLFormElement>): Promise<void> => {
    event.preventDefault();

    const response = await fetch('http://localhost:8000/create/guest/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ name: str1,
      cpf: str2,
      nickname: str3,
      relationship: str4}),
    });

    if (response.ok) {
      console.log('Strings enviadas com sucesso!');
    } else {
      console.error('Erro ao enviar as strings!');
    }
  };

  const handlePhotoInputChange = (event: ChangeEvent<HTMLInputElement>) => {
    const files = event.target.files;
    if (files) {
      const selectedFiles = Array.from(files).slice(0, 5); // Limitando a seleção a 5 fotos
      setPhotoFiles(selectedFiles);
    }
  };

  const handlePhotoSubmit = async (event: FormEvent<HTMLFormElement>): Promise<void> => {
    event.preventDefault();

    const formData = new FormData();
    photoFiles.forEach((file, index) => {
      formData.append('image${index + 1}', file);
    });

    const response = await fetch('http://localhost:8000/api/photos/', {
      method: 'POST',
      body: formData,
    });

    if (response.ok) {
      console.log('Fotos enviadas com sucesso!');
    } else {
      console.error('Erro ao enviar as fotos!');
    }
  };

  return (
    <div>
      <h1>Aplicação</h1>

      <h2>Soma de Variáveis</h2>
      <form onSubmit={handleFormSubmit}>
        <label>
          Variável 1:
          <input type="number" value={var1} onChange={(event) => handleInputChange(event, setVar1)} />
        </label>
        <br />
        <label>
          Variável 2:
          <input type="number" value={var2} onChange={(event) => handleInputChange(event, setVar2)} />
        </label>
        <br />
        <button type="submit">Somar</button>
      </form>
      <p>Resultado: {resultado}</p>

      <h2>Enviar Strings</h2>
      <form onSubmit={handleStringsSubmit}>
        <label>
          String 1:
          <input type="text" value={str1} onChange={(event) => handleInputChange(event, setStr1)} />
        </label>
        <br />
        <label>
          String 2:
          <input type="text" value={str2} onChange={(event) => handleInputChange(event, setStr2)} />
        </label>
        <br />
        <label>
          String 3:
          <input type="text" value={str3} onChange={(event) => handleInputChange(event, setStr3)} />
        </label>
        <br />
        <label>
          String 4:
          <input type="text" value={str4} onChange={(event) => handleInputChange(event, setStr4)} />
        </label>
        <br />
        <button type="submit">Enviar Strings</button>
      </form>
      <h2>Upload de Fotos</h2>
      <form onSubmit={handlePhotoSubmit}>
        <label>
          Foto 1:
          <input type="file" onChange={handlePhotoInputChange} accept="image/*" multiple />
        </label>
        <br />
        {/* Adicione mais inputs para as outras fotos */}
        <button type="submit">Enviar Fotos</button>
      </form>
    </div>
  );
};

export default App;