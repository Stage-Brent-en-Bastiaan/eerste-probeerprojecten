import React from "react";
import { Link } from "react-router-dom";
import StyledNavLink from "./StyledNavLink";



const Header = () => {


  return (
    <div className="bg-blue-600 p-2 text-white shadow-lg">
      <Link
        to="/"
        className="font-black text-xl text-white no-underline hover:underline">
        StageApp
      </Link>
      <div className="flex justify-end items-center gap-4 ">
        <StyledNavLink to="/" className="text-400">
          Home
        </StyledNavLink>
        <StyledNavLink to="/patients">Patients</StyledNavLink>
        <StyledNavLink to="/tasks">Tasks</StyledNavLink>
        <StyledNavLink to="/newtask">New Task</StyledNavLink>
      </div>
    </div>
  );
};

export default Header;
