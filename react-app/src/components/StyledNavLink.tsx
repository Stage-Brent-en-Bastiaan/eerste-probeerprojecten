import React from "react";
import { NavLink } from "react-router-dom";

const StyledNavLink = (props: React.ComponentProps<typeof NavLink>) => {
  return (
    <NavLink
      {...props}
      className={({ isActive }) =>
        `${
          isActive
            ? "text-white underline underline-offset-4"
            : "text-gray-300 no-underline"
        } ${props.className}`
      }
    />
  );
};
export default StyledNavLink;
