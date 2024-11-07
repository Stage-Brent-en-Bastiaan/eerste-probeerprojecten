import React from 'react'
import ReactDOM from 'react-dom/client'
import './index.css'
import { createBrowserRouter, RouterProvider } from 'react-router-dom'
import RootLayout from './navigation/RootLayout';
import HomePage from './pages/Homepage';
import PatientsPage from './pages/PatientsPage';
import NewTask from './pages/NewTask';
import TasksPage from './pages/TasksPage';
import 'bootstrap/dist/css/bootstrap.min.css';


const browserRouter = createBrowserRouter([
  {
    path: "/",
    element: <RootLayout />,
    children: [
      {
        // index: true,
        path: "/",
        element: <HomePage />,
      },
     
      {
        path: "newTask",
        element: <NewTask />,
      },
      {
        path: "patients",
        element: <PatientsPage />,
      },
      {
        path: "tasks",
        element: <TasksPage />,
      }
    ],
  },
]);

// test


ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    <RouterProvider router={browserRouter}></RouterProvider>
  </React.StrictMode>
)