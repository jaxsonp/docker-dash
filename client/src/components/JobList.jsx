import { Table, Button, Form, Spinner, Pagination } from "react-bootstrap";
import { ChevronDown, ChevronUp } from "react-feather";
import { useState, useEffect } from "react";
import handleFetch from "../handleFetch";
import Chart from "./Chart";
import { redirect, useParams } from "react-router-dom";
import ReactJson from "@microlink/react-json-view";
import ImportModal from "./ImageModal";
import { DangerModal } from "./ImageModal";
// import services from "../services.json";
// import containers from "../db.json";
// import images from "../images.json";

const renderPagination = (items, step, selectedIndex, setSelectedIndex) => {
  let pages = [];
  for (let i = 1; i <= Math.ceil(items / step); i++) {
    pages.push(
      <Pagination.Item
        active={selectedIndex === i}
        onClick={() => setSelectedIndex(i)}
        key={i}
      >
        {i}
      </Pagination.Item>
    );
  }
  return pages;
};

// function updateListOnSuccess(checkedRows) {

// }

// revise this to only take the dynamic part of api i.e. stop, start, etc.
async function handleBatchPost(arrayOfArrays, api, originalArray, newState) {
  let commaSeparated = [];
  for (let i = 0; i < arrayOfArrays.length; i++) {
    commaSeparated.push(arrayOfArrays[i][0]);
  }
  let commaStrung = commaSeparated.join(",");

  let url = api + commaStrung;

  let response;
  try {
    response = await fetch(url, {
      method: "POST",
    });
    response = await response.json();
  } catch (err) {
    console.error(err);
  }

  if (response.status === 200) {
    let toRevise = originalArray.map((x) => Object.assign({}, x));
    let mappedRevised = toRevise
      .filter((el) => commaSeparated.includes(el.Names))
      .map(
        (el) => (el.State = newState !== "restarting" ? newState : "running")
      );
    let updatedArray = null;
    if (newState !== "banished") {
      updatedArray = toRevise.map((obj) =>
        obj.Names === mappedRevised.Names ? mappedRevised : obj
      );
    } else {
      toRevise.forEach(
        (el, index) => el.State === "banished" && toRevise.splice(index, 1)
      );
      updatedArray = toRevise;
    }
    return updatedArray;
  }
}

const api = "http://192.168.98.74/api/demo/";
const step = 10;

export default function JobList() {
  const [directory, setDirectory] = useState("");
  const [order, setOrder] = useState([]);
  const [sortConfig, setSortConfig] = useState({
    key: null,
    direction: "asc",
  });
  const [inView, setInView] = useState({
    labels: null,
    key: null,
    performance: null,
    details: null,
  });
  const [loading, setLoading] = useState("");
  const [checkedRows, setCheckedRows] = useState([]);
  const [relevantResults, setRelevantResults] = useState([]);
  const [filterQuery, setFilterQuery] = useState("");
  const { view, viewId } = useParams();
  const [sortableHeaders, setSortableHeaders] = useState([]);
  const [modalShow, setModalShow] = useState(false);
  const [selectedIndex, setSelectedIndex] = useState(1);
  // const [reorderedData, setReorderedData] = useState([]);
  const [failed, setFailed] = useState(false);
  const [numItems, setNumItems] = useState(1);
  const [dangerShow, setDangerShow] = useState(false);

  const appHeaders = ["ID", "State", "Image", "Names", "CreatedAt"];
  const appButtons = [
    {
      name: "Start",
      disabledBy: ["restarting", "running", "paused", "dead"],
      causes: "running",
      api: api + "start-app?name=",
    },
    {
      name: "Stop",
      disabledBy: ["created", "restarting", "exited", "dead"],
      causes: "exited",
      api: api + "stop-app?name=",
    },
    {
      name: "Pause",
      disabledBy: ["created", "restarting", "paused", "exited", "dead"],
      causes: "paused",
      api: api + "pause-app?name=",
    },
    {
      name: "Resume",
      causes: "running",
      disabledBy: ["created", "running", "restarting", "exited", "dead"],
      api: api + "unpause-app?name=",
    },
    {
      name: "Restart",
      disabledBy: ["created", "restarting", "exited", "dead"],
      causes: "restarting",
      api: api + "restart-app?name=",
    },
    {
      variant: "warning",
      name: "Kill",
      causes: "exited",
      disabledBy: ["created", "exited", "dead"],
      api: api + "kill-app?name=",
    },
  ];
  const imageHeaders = ["Repository", "Size", "Containers", "Tag", "CreatedAt"];
  // const serviceHeaders = [
  //   "Name",
  //   "ID",
  //   "BlockIO",
  //   "NetIO",
  //   "CPUPerc",
  //   "MemUsage",
  // ];

  useEffect(() => {
    setFailed(false);
    let timer = setTimeout(() => {
      order.length === 0 && setFailed(true);
    }, 5000);
    return () => clearTimeout(timer);
  }, [view]);

  useEffect(() => {
    let timer = setInterval(() => {
      sessionStorage.removeItem("apps");
      sessionStorage.removeItem("images");
      sessionStorage.removeItem("inspectApp");
      sessionStorage.removeItem("appHealth");
    }, 300000);
    return () => clearInterval(timer);
  }, []);

  useEffect(() => {
    async function getExpectedData() {
      setOrder([]);
      setRelevantResults([[{ Id: "Loading..." }]]);
      setCheckedRows([]);
      if (view === "apps") {
        setDirectory("apps");
        setSortableHeaders(appHeaders);
        try {
          let apps = await handleFetch("apps", api + "get-app-status");
          setOrder(apps);
          sessionStorage.setItem("apps", JSON.stringify(apps));
        } catch (err) {
          setFailed(true);
          console.error(err);
        }
        if (viewId) {
        }
      } else if (view === "images") {
        setDirectory("images");
        setSortableHeaders(imageHeaders);
        try {
          let images = await handleFetch("images", api + "get-images");
          setOrder(images);
        } catch (err) {
          setFailed(true);
          console.error(err);
        }
        if (viewId) {
        }
      } else {
        setOrder([]);
      }
    }
    getExpectedData();
  }, [view, viewId]);

  useEffect(() => {
    setNumItems(order.length);
  }, [order.length]);

  useEffect(() => {
    if (order && order.length) {
      let displayedCards = order.slice(
        selectedIndex * step - step,
        selectedIndex * step
      );
      setRelevantResults(displayedCards || order.slice(0, 10));
    }
  }, [order, selectedIndex, numItems]);

  useEffect(() => {
    let relevant = [];
    if (order && order.length) {
      if (!filterQuery.length) {
        setRelevantResults(order.slice(0, 10));
      } else {
        for (let obj of order) {
          let objValues = Object.values(obj);
          objValues = objValues.filter((val) => typeof val === "string");
          if (objValues.some((x) => x.includes(filterQuery))) {
            relevant.push(obj);
          }
          setRelevantResults(relevant);
        }
      }
    }
  }, [order, filterQuery]);

  function handleChange(e, containerId, containerState) {
    if (directory === "images") {
      if (e.target.checked) {
        setCheckedRows([containerId]);
      }
    } else if (directory === "apps") {
      if (e.target.checked) {
        if (!checkedRows.flat().includes(containerId)) {
          setCheckedRows([...checkedRows, [containerId, containerState]]);
        }
      } else {
        let indexToRemove = checkedRows.findIndex((nested) =>
          nested.includes(containerId)
        );
        let preserved = [
          ...checkedRows
            .slice(0, indexToRemove)
            .concat(checkedRows.slice(indexToRemove + 1, checkedRows.length)),
        ];
        setCheckedRows(preserved);
      }
    }
  }

  function sortDataBy(key) {
    if (!order || !order.length) return;
    let direction = "asc";
    if (sortConfig.key === key && sortConfig.direction === "asc") {
      direction = "desc";
    }

    let sortedData;
    if (key !== "id") {
      sortedData = order.slice().sort((a, b) => {
        const valueA = a[key] ? a[key].toLowerCase() : "";
        const valueB = b[key] ? b[key].toLowerCase() : "";

        if (!valueA && !valueB) {
          return 0;
        } else if (!valueA) {
          return direction === "asc" ? 1 : -1;
        } else if (!valueB) {
          return direction === "asc" ? -1 : 1;
        }

        if (valueA > valueB) {
          return direction === "asc" ? 1 : -1;
        } else if (valueA < valueB) {
          return direction === "asc" ? -1 : 1;
        } else {
          return 0;
        }
      });
    } else {
      sortedData = order.slice().sort((a, b) => {
        if (a[key] === null && b[key] === null) {
          return 0;
        } else if (a[key] === null) {
          return direction === "asc" ? 1 : -1;
        } else if (b[key] === null) {
          return direction === "asc" ? -1 : 1;
        }

        return direction === "asc" ? a[key] - b[key] : b[key] - a[key];
      });
    }

    setOrder(sortedData);
    setSortConfig({ key, direction });
  }

  async function handleChartUpdate() {
    let inspectApp;
    try {
      inspectApp = await fetch(api + `get-app-info?name=${checkedRows[0][0]}`);
      inspectApp = await inspectApp.json();
    } catch (err) {
      console.error(err);
    }

    let appHealth;
    try {
      appHealth = await fetch(
        api + `get-uptime-summary?name=${checkedRows[0][0]}&duration=hour`
      );
      appHealth = await appHealth.json();
    } catch (err) {
      console.error(err);
    }

    let appHealthLabels = Object.keys(appHealth).map((val) =>
      val.substring(11, 16)
    );
    let appHealthToNums = Object.values(appHealth).map((val) => +val);

    setInView({
      labels: appHealthLabels,
      key: checkedRows[0][0],
      performance: appHealthToNums,
      details: inspectApp,
    });
  }

  return (
    <>
      {(view === "images" || view === "apps") && order && order.length > 0 ? (
        <>
          <ImportModal show={modalShow} onHide={() => setModalShow(false)} />
          <DangerModal
            show={dangerShow}
            onHide={() => setDangerShow(false)}
            handleBatchPost={async () =>
              await handleBatchPost(
                checkedRows,
                api + "delete-app?name=",
                order,
                "banished"
              ).then((res) => {
                setOrder(res);
                setCheckedRows([]);
              })
            }
          />
          {/* {directory !== "images" && (
            <div
              style={{
                display: "flex",
                margin: "20px",
                gap: "15px",
                justifyContent: "center",
                alignItems: "center",
              }}
            >
              <Form.Control
                value={filterQuery}
                onChange={(e) => setFilterQuery(e.target.value)}
                style={{ width: "300px", height: "38px" }}
                type="text"
                placeholder="Get Specific User"
              ></Form.Control>
              <Button>Get</Button>
            </div>
          )} */}
          <div
            style={{
              display: "flex",
              margin: "20px",
              gap: "40px",
              justifyContent: "center",
              alignItems: "flex-end",
            }}
          >
            <Form.Control
              value={filterQuery}
              onChange={(e) => setFilterQuery(e.target.value)}
              style={{ width: "300px", height: "38px", marginBottom: "-4px" }}
              type="text"
              placeholder="Search table for..."
              size="sm"
            ></Form.Control>
            <div
              style={{
                display: "flex",
                gap: "20px",
                flexWrap: "wrap",
              }}
            >
              {directory === "apps" ? (
                <>
                  <Button
                    onClick={handleChartUpdate}
                    disabled={
                      checkedRows.length > 1 || checkedRows.length === 0
                    }
                    size="sm"
                  >
                    Inspect (One)
                  </Button>
                  {appButtons.map((button, key) => (
                    <Button
                      key={key}
                      variant={button.variant || "primary"}
                      size="sm"
                      disabled={
                        checkedRows.length === 0 ||
                        checkedRows
                          .flat()
                          .some((el) => button["disabledBy"].includes(el)) ||
                        loading
                      }
                      onClick={async () => {
                        setLoading(button.name);
                        let newOrder = await handleBatchPost(
                          checkedRows,
                          button.api,
                          order,
                          button.causes
                        );
                        setOrder(newOrder);
                        alert("200 Request Successful");
                        setLoading("");
                        setCheckedRows([]);
                      }}
                    >
                      {loading === button.name ? (
                        <div style={{ width: button.name.length - 1 + "ch" }}>
                          <Spinner size="sm" animation="border" />
                        </div>
                      ) : (
                        button.name
                      )}
                    </Button>
                  ))}
                  {
                    <Button
                      size="sm"
                      variant="danger"
                      disabled={
                        checkedRows.length === 0 ||
                        checkedRows
                          .flat()
                          .some((el) =>
                            ["paused", "restarting", "running"].includes(el)
                          ) ||
                        loading
                      }
                      onClick={() => setDangerShow(true)}
                    >
                      Remove
                    </Button>
                  }
                </>
              ) : directory === "images" ? (
                <>
                  <Button size="sm" onClick={() => setModalShow(true)}>
                    Request Image
                  </Button>
                  <Button
                    onClick={async () => {
                      try {
                        let response = await fetch(
                          api +
                            "create-app?image=" +
                            checkedRows[0] +
                            "&user=janeschmo",
                          {
                            method: "POST",
                          }
                        );
                        response = await response.json();
                        return redirect("/apps");
                      } catch (err) {
                        console.error(err);
                      }
                    }}
                    disabled={checkedRows.length === 0}
                    size="sm"
                  >
                    Create App
                  </Button>
                </>
              ) : (
                <Button
                  variant="warning"
                  disabled={checkedRows.length === 0}
                  size="sm"
                >
                  Kill Service
                </Button>
              )}
            </div>
          </div>
          <Table style={{ marginBottom: 0 }} responsive striped bordered>
            <thead>
              <tr>
                {directory === "apps" ? (
                  <>
                    <th>
                      <div
                        onClick={() =>
                          checkedRows.length > 0
                            ? setCheckedRows([])
                            : setCheckedRows(
                                relevantResults.map((container) => [
                                  container.Names
                                    ? container.Names
                                    : container.Repository,
                                  container.State,
                                ])
                              )
                        }
                      >
                        Enable Actions
                        <br />
                        (Selected: {checkedRows.length})
                      </div>
                    </th>
                  </>
                ) : directory === "images" ? (
                  <>
                    <th className="nohover">
                      <div>Enable Actions</div>
                    </th>
                  </>
                ) : (
                  <></>
                )}
                {sortableHeaders.map((header, key) => {
                  return (
                    <th key={key} onClick={() => sortDataBy(header)}>
                      <div>
                        {header + " "}
                        {sortConfig.key === header ? (
                          sortConfig.direction === "asc" ? (
                            <ChevronUp size={15} />
                          ) : (
                            <ChevronDown size={15} />
                          )
                        ) : (
                          <ChevronUp size={15} color="transparent" />
                        )}
                      </div>
                    </th>
                  );
                })}
              </tr>
            </thead>
            <tbody>
              {(relevantResults.length > 0 ? relevantResults : order).map(
                (datum, key) => {
                  return (
                    <tr key={key}>
                      <td style={{ padding: 0 }}>
                        <label
                          className="grayify"
                          style={{
                            padding: "20px 0",
                            width: "100%",
                          }}
                        >
                          <input
                            onChange={(e) =>
                              handleChange(
                                e,
                                datum.Names ||
                                  datum.Repository + ":" + datum.Tag,
                                datum.State || ""
                              )
                            }
                            value={
                              datum.Names
                                ? datum.Names
                                : datum.Repository + ":" + datum.Tag
                            }
                            checked={checkedRows
                              .flat()
                              .includes(
                                datum.Names
                                  ? datum.Names
                                  : datum.Repository + ":" + datum.Tag
                              )}
                            type={directory === "apps" ? "checkbox" : "radio"}
                          ></input>
                        </label>
                      </td>
                      {sortableHeaders.map((header, key) => {
                        return (
                          <>
                            <td
                              style={{
                                maxWidth: "180px",
                                overflowWrap: "break-word",
                              }}
                              key={key}
                            >
                              {datum[header]}
                            </td>
                          </>
                        );
                      })}
                    </tr>
                  );
                }
              )}
            </tbody>
          </Table>
          <Pagination
            style={{
              width: "fit-content",
              margin: "15px auto",
              display: "flex",
              justifyContent: "center",
            }}
          >
            <Pagination.First
              onClick={() => {
                setSelectedIndex(1);
              }}
            />
            <Pagination.Prev
              onClick={() =>
                selectedIndex > 1 && setSelectedIndex(selectedIndex - 1)
              }
            />
            {renderPagination(numItems, step, selectedIndex, setSelectedIndex)}
            <Pagination.Next
              onClick={() =>
                selectedIndex < Math.ceil(order.length / step) &&
                setSelectedIndex(selectedIndex + 1)
              }
            />
            <Pagination.Last
              onClick={() => setSelectedIndex(Math.ceil(order.length / step))}
            />
          </Pagination>

          {directory === "apps" && (
            <div
              style={{
                display: "flex",
                gap: "10px",
                justifyContent: "space-around",
              }}
            >
              <ReactJson
                style={{
                  textAlign: "left",
                  wordBreak: "break-all",
                }}
                collapsed={false}
                src={
                  order &&
                  order.length &&
                  order[order.findIndex((el) => el.Names === inView.key)]
                }
              />
              <div
                style={{
                  height: "60dvh",
                  width: "800px",
                }}
              >
                <Chart inView={inView} />
              </div>
            </div>
          )}
        </>
      ) : !view === "images" && !view === "apps" ? (
        <div style={{ height: "90dvh", display: "grid", placeItems: "center" }}>
          <h1>404 Page Not Found</h1>
        </div>
      ) : failed ? (
        <h2 style={{ color: "crimson" }}>Something went wrong...</h2>
      ) : (
        <div style={{ height: "484px" }}>
          <Spinner animation="border" />
        </div>
      )}
    </>
  );
}
