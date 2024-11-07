import React, { useState } from "react";
import Button from "react-bootstrap/Button";
import Col from "react-bootstrap/Col";
import Form from "react-bootstrap/Form";
import Row from "react-bootstrap/Row";

interface Task {
  task_type: string;
  payload: JSON;
  status: string;
  retries: number;
  priority: number;
}

const NewTask: React.FC = () => {
  const [newTask, setNewTask] = useState<Task>({
    task_type: "send_message",
    payload: JSON.parse("{}"),
    status: "in_queue",
    retries: 0,
    priority: 0,
  });
  const [hospitalId, setHospitalId] = useState<string>("9203161015");
  const [message, setMessage] = useState<string>("");
  const [fileName, setFileName] = useState<string>("");
  const [title, setTitle] = useState<string>("");
  const [fileData, setFileData] = useState<string>("");
  const [error, setError] = useState<string | null>(null);

  const handleTaskChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    setNewTask({ ...newTask, [event.target.name]: event.target.value });
  };

  const handleHospitalIdChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    setHospitalId(event.target.value);
  };

  const handleMessageChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    setMessage(event.target.value);
  };
  // const handleFileNameChange = (event: React.ChangeEvent<HTMLInputElement>) => {
  //   setFileName(event.target.value);
  // };
  const handleTitleChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    setTitle(event.target.value);
  };
  const handleFileChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (file) {
      setFileName(file.name);
      const reader = new FileReader();
      reader.onloadend = () => {
        const base64String = reader.result?.toString().split(",")[1] || ""; 
        setFileData(base64String);
      };
      reader.readAsDataURL(file);
    }
  };

  const handleSubmit = async (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    try {
      // Zet de JSON-string voor payload met hospital_id en message
      // const payload = `{ hospital_id: ${hospitalId}, message: ${message} }`;
      const payload = { hospital_id: hospitalId, message: message, title:title, files:[
        {
          "filename": fileName,
          "data": fileData,
        }
      ] };

      const taskData = { ...newTask, payload };

      const response = await fetch("http://172.24.103.220:8000/api/tasks?format=json", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(taskData),
      });

      if (!response.ok) {
        throw new Error("Failed to create task");
      }

      // Reset de velden
      setNewTask({
        task_type: "send_message",
        payload: "",
        status: "in_queue",
        retries: 0,
        priority: 0,
      });
      setHospitalId("");
      setMessage("");
      setFileName("");
      setTitle("");
      setFileData("");
      setError(null);
    } catch (error) {
      setError("Fout: " + error);
    }
  };

  return (
    <Form onSubmit={handleSubmit}>
      <Form.Group className="mb-3">
        <Form.Label>Task Type</Form.Label>
        <Form.Control
          type="text"
          name="task_type"
          value={newTask.task_type}
          onChange={handleTaskChange}
        />
      </Form.Group>
      <Form.Group className="mb-3">
        <Form.Label>Hospital ID</Form.Label>
        <Form.Control
          type="text"
          name="hospital_id"
          value={hospitalId}
          onChange={handleHospitalIdChange}
        />
      </Form.Group>
      <Form.Group className="mb-3">
        <Form.Label>Title</Form.Label>
        <Form.Control
          type="text"
          name="title"
          value={title}
          onChange={handleTitleChange}
        />
      </Form.Group>
      <Form.Group className="mb-3">
        <Form.Label>Message</Form.Label>
        <Form.Control
          type="text"
          name="message"
          value={message}
          onChange={handleMessageChange}
        />
      </Form.Group>
      <Form.Group className="mb-3">
        <Form.Label>Status</Form.Label>
        <Form.Control
          type="text"
          name="status"
          value={newTask.status}
          onChange={handleTaskChange}
        />
      </Form.Group>
      <Form.Group className="mb-3">
        <Form.Label>Retries</Form.Label>
        <Form.Control
          type="number"
          name="retries"
          value={newTask.retries}
          onChange={handleTaskChange}
        />
      </Form.Group>
      <Form.Group className="mb-3">
        <Form.Label>Priority</Form.Label>
        <Form.Control
          type="number"
          name="priority"
          value={newTask.priority}
          onChange={handleTaskChange}
        />
        </Form.Group>
      {/* <Form.Group className="mb-3">
        <Form.Label>File Name</Form.Label>
        <Form.Control
        type="text"
        name="filename"
        value={fileName}
        onChange={handleFileNameChange}
        />
      </Form.Group> */}
      <Form.Group className="mb-3">
        <Form.Label>Upload PDF</Form.Label>
        <Form.Control
          type="file"
          accept="application/pdf"
          onChange={handleFileChange} 
        />
      </Form.Group>
      <Button variant="primary" type="submit">
        Submit
      </Button>
      {error && <p>{error}</p>}
    </Form>
  );
};

export default NewTask;
