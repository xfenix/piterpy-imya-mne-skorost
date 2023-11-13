import http from "k6/http";
import { sleep } from "k6";

export const options = {
  stages: [
    { duration: "20s", target: 100 },
    { duration: "30s", target: 1000 },
    { duration: "20s", target: 100 },
  ],
};

export default function () {
  http.get("http://37.230.112.113/test/simple/");
  sleep(0.2);
}
