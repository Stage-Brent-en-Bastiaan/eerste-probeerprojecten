import React, { useState, useEffect } from "react";
import axios from "axios";
import { Button, Table } from "react-bootstrap";

interface Task {
  id: number;
  task_type: string;
  payload: {
    hospital_id: string;
    message: string;
  };
  status: string;
  statuslog: string;
  retries: number;
  priority: number;
  // created_at: string;
  // updated_at: string;
  // processed_at: string;
  logTeller: number;
}

const TasksPage: React.FC = () => {
  const [tasks, setTasks] = useState<Task[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);
  const [sortAscending, setSortAscending] = useState<boolean>(true);

  useEffect(() => {
    const fetchTasks = async () => {
      try {
        const response = await axios.get("http://172.24.103.220:8000/api/tasks?format=json");
        const parsedData = JSON.parse(response.data);  
        setTasks(parsedData);
        setLoading(false);
      } catch (error) {
        setError("Er is een fout opgetreden bij het ophalen van de gegevens.");
        setLoading(false);
      }
    };

    fetchTasks();
  }, []);

  const sortTasksById = () => {
    const sortedTasks = [...tasks].sort((a, b) => {
      return sortAscending ? a.id - b.id : b.id - a.id;
    });
    setTasks(sortedTasks);
    setSortAscending(!sortAscending);
  };

  if (loading) {
    return <p>Gegevens worden geladen...</p>;
  }

  if (error) {
    return <p>{error}</p>;
  }

  const handleExecuteTasks = async () => {
    try {
      const response = await axios.get('http://172.24.103.220:8000/api/executetasks');
      console.log('Response data:', response.data);
    } catch (error) {
      console.error('Error executing tasks:', error);
    }
  };

  return (
    <div>
      <Button onClick={handleExecuteTasks}>
        Execute Tasks
      </Button>
      <h1>Takenlijst</h1>
      <Table striped bordered hover size="sm">
        <thead>
          <tr>
          <th onClick={sortTasksById} style={{ cursor: "pointer" }}>
              ID {sortAscending ? "↑" : "↓"}
            </th>
            <th>Taaktype</th>
            <th>Ziekenhuis ID</th>
            <th>Bericht</th>
            <th>Status</th>
            <th>Retries</th>
            <th>Prioriteit</th>
            <th>Aangemaakt</th>
            <th>Bewerkt</th>
          </tr>
        </thead>
        <tbody>
          {tasks.map((task) => (
            <tr key={task.id}>
              <td>{task.id}</td>
              <td>{task.task_type}</td>
              <td>{task.payload.hospital_id}</td>
              <td>{task.payload.message}</td>
              <td>{task.status}</td>
              <td>{task.retries}</td>
              <td>{task.priority}</td>
              <td>{task.created_at.substring(0, 16)}</td>
              <td>{task.updated_at ? task.updated_at.substring(0, 16) : ''}</td>
              </tr>
          ))}
        </tbody>
      </Table>
    </div>
  );
};

export default TasksPage;
