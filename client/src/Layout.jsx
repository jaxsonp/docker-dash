import { NavLink, Outlet } from "react-router-dom";
import { Button } from "react-bootstrap";
import { ArrowUp } from "react-feather";

export default function Layout() {
  return (
    <>
      <Button
        style={{
          position: "fixed",
          bottom: "10px",
          right: "10px",
          zIndex: 1,
          opacity: 0.8,
          padding: "6px 3px",
        }}
        onClick={() => window.scrollTo({ top: 0, behavior: "instant" })}
      >
        <ArrowUp />
      </Button>
      <nav
        style={{
          backgroundColor: "navy",
          color: "gainsboro",
        }}
      >
        <ul
          style={{
            height: "max(60px, 11dvh)",
            display: "flex",
            listStyle: "none",
            padding: 0,
            justifyContent: "space-evenly",
            alignItems: "center",
          }}
        >
          <li>
            <NavLink
              className={({ isActive }) => (isActive ? "active" : "")}
              to="/"
            >
              View Servers
            </NavLink>
          </li>
          <li>
            <NavLink
              className={({ isActive }) => (isActive ? "active" : "")}
              to="/apps"
            >
              View Apps
            </NavLink>
          </li>
          <li>
            <NavLink
              className={({ isActive }) => (isActive ? "active" : "")}
              to="/images"
            >
              View Images
            </NavLink>
          </li>
        </ul>
      </nav>
      <Outlet />
    </>
  );
}
