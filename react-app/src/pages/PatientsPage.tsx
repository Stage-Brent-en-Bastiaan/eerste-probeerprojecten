import React, { useState, useEffect } from 'react';
import axios from 'axios';
import Table from 'react-bootstrap/Table';

interface Patient {
  id: number;
  box_code: string;
  first_name: string;
  last_name: string;
  phone_contact: string;
  phone_auth: string;
  gov_id: string | null;
  hospital_id: string;
  date_of_birth: string;
  gender: string;
  address: string | null;
  nationality: string | null;
  locale: string;
}


const PatientsPage: React.FC = () => {
  const [patients, setPatients] = useState<Patient[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchPatients = async () => {
      try {
        const response = await axios.get("http://172.24.103.220:8000/api/patients?format=json");
        const parsedData = JSON.parse(response.data);
        setPatients(parsedData);
        setLoading(false);
      } catch (error) {
        setError("Er is een fout opgetreden bij het ophalen van de gegevens.");
        setLoading(false);
      }
    };

    fetchPatients();
  }, []);

  if (loading) {
    return <p>Gegevens worden geladen...</p>;
  }

  if (error) {
    return <p>{error}</p>;
  }

  return (
    <div>
      <h1>Patientenlijst</h1>
      <Table striped bordered hover size='sm'>
        <thead>
          <tr>
            <th>ID</th>
            <th>Box Code</th>
            <th>Voornaam</th>
            <th>Achternaam</th>
            <th>Telefoon</th>
            <th>Gov ID</th>
            <th>Ziekenhuis ID</th>
            <th>Geboortedatum</th>
            <th>Geslacht</th>
            <th>Nationaliteit</th>
            <th>Taal</th>
          </tr>
        </thead>
        <tbody>
          {patients.map((patient) => (
            <tr key={patient.id}>
              <td>{patient.id}</td>
              <td>{patient.box_code}</td>
              <td>{patient.first_name}</td>
              <td>{patient.last_name}</td>
              <td>{patient.phone_contact}</td>
              <td>{patient.gov_id ?? "Geen"}</td>
              <td>{patient.hospital_id}</td>
              <td>{patient.date_of_birth}</td>
              <td>{patient.gender}</td>
              <td>{patient.nationality ?? "Geen"}</td>
              <td>{patient.locale}</td>
            </tr>
          ))}
        </tbody>
      </Table>
    </div>
  );
};

export default PatientsPage;