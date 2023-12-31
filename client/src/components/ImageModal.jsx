import { Button } from "react-bootstrap";
import { Modal } from "react-bootstrap";
import { Form } from "react-bootstrap";
import { Spinner } from "react-bootstrap";
import ReactJson from "@microlink/react-json-view";
import { useRef, useState } from "react";

const api = "http://192.168.98.74/api/demo/";

export default function ImportModal(props) {
  const imageRef = useRef();
  const reasonRef = useRef();
  const [loading, setLoading] = useState(false);

  return (
    <Modal
      {...props}
      size="lg"
      aria-labelledby="contained-modal-title-vcenter"
      centered
    >
      <Modal.Header closeButton style={{ background: "gainsboro" }}>
        <Modal.Title
          id="contained-modal-title-vcenter"
          style={{ width: "100%", textAlign: "center" }}
        >
          Image Request Center
        </Modal.Title>
      </Modal.Header>
      <Modal.Body>
        <h4>Which dockerhub image are you looking for?</h4>
        <Form.Control ref={imageRef} type="text"></Form.Control>
        <h4>Reasons for Request:</h4>
        <Form.Control ref={reasonRef} as="textarea" rows={3}></Form.Control>
      </Modal.Body>
      <Modal.Footer>
        <div style={{ margin: "auto" }}>
          <Button
            style={{ marginRight: "50px", width: loading ? "5ch" : "initial" }}
            disabled={loading}
            onClick={async () => {
              setLoading(true);
              let response = await fetch(
                api + "request-image?image=" + imageRef.current.value,
                {
                  method: "POST",
                }
              );
              if (response.ok === true) {
                alert("200 Request Successful");
                imageRef.current.value = "";
                reasonRef.current.value = "";
              } else {
                alert("Something went wrong...");
              }
              setLoading(false);
              props.onHide();
            }}
          >
            {loading ? <Spinner size="sm" animation="border" /> : "Submit"}
          </Button>
          <Button variant="warning" onClick={() => props.onHide()}>
            Cancel
          </Button>
        </div>
      </Modal.Footer>
    </Modal>
  );
}

export function DangerModal(props) {
  return (
    <Modal
      {...props}
      size="lg"
      aria-labelledby="contained-modal-title-vcenter"
      centered
    >
      <Modal.Header closeButton style={{ background: "gainsboro" }}>
        <Modal.Title
          id="contained-modal-title-vcenter"
          style={{ width: "100%", textAlign: "center" }}
        >
          Do you want to remove selected app(s)?
        </Modal.Title>
      </Modal.Header>
      <Modal.Footer>
        <div style={{ margin: "auto" }}>
          <Button
            style={{ marginRight: "50px" }}
            onClick={async () => {
              props.onHide();
              await props.handleBatchPost();
            }}
          >
            Yes
          </Button>
          <Button variant="warning" onClick={() => props.onHide()}>
            No
          </Button>
        </div>
      </Modal.Footer>
    </Modal>
  );
}

export function InspectModal(props) {
  return (
    <Modal
      {...props}
      size="lg"
      aria-labelledby="contained-modal-title-vcenter"
      centered
    >
      <Modal.Header closeButton style={{ background: "gainsboro" }}>
        <Modal.Title
          id="contained-modal-title-vcenter"
          style={{ width: "100%", textAlign: "center" }}
        >
          {"<server.hostname>"}
        </Modal.Title>
      </Modal.Header>
      <Modal.Body>
        <ReactJson
          style={{
            textAlign: "left",
            wordBreak: "break-all",
          }}
          collapsed={false}
          src={props.src}
        />
      </Modal.Body>
    </Modal>
  );
}
