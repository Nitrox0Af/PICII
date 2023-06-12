import React, { useState, ChangeEvent, FormEvent } from 'react';
import axios, { AxiosResponse } from 'axios';

interface FormFields {
  cpf: string;
  name: string;
  surname: string;
  relationship: string;
}

const InputsData: React.FC = () => {
  const [formData, setFormData] = useState<FormFields>({
    cpf: '',
    name: '',
    surname: '',
    relationship: '',
  });

  const handleChange = (event: ChangeEvent<HTMLInputElement>) => {
    const { name, value } = event.target;
    setFormData((prevFormData) => ({
      ...prevFormData,
      [name]: value,
    }));
  };

  const handleSubmit = async (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault();

    try {
      const response: AxiosResponse = await axios.post('/api/form/', formData);
      console.log(response.data); // Exibe a resposta do servidor no console
    } catch (error) {
      console.error(error);
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      <input
        className="cpf"
        type="text"
        name="cpf"
        value={formData.cpf}
        onChange={handleChange}
        placeholder="CPF"
      />
      <input
      className='name'
        type="text"
        name="name"
        value={formData.name}
        onChange={handleChange}
        placeholder="Nome"
      />
      <input
      className='surname'
        type="text"
        name="surname"
        value={formData.surname}
        onChange={handleChange}
        placeholder="Sobrenome"
      />
      <input
        className='relationship'
        type="text"
        name="relationship"
        value={formData.relationship}
        onChange={handleChange}
        placeholder="Relacionamento"
      />
      <button className='upload' type="submit">Enviar</button>
    </form>
  );
};

export default InputsData;