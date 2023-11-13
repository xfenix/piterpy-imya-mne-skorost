import http from "k6/http";
import { sleep } from "k6";

const POSSIBE_DASHBOARD_TYPES = [1, 2, 3];
const genRandomNumber = (min, max) => {
  return Math.random() * (max - min) + min;
};
const genRandomDate = (from = new Date(2023, 0, 1), to = new Date()) => {
  return new Date(
    from.getTime() + Math.random() * (to.getTime() - from.getTime())
  );
};
export const options = {
  stages: [
    { duration: "20s", target: 100 },
    { duration: "30s", target: 1000 },
    { duration: "20s", target: 100 },
  ],
};

export default function () {
  http.post(
    "http://37.230.112.113/test/complex/",
    JSON.stringify({
      user_name: (Math.random() + 1).toString(36).substring(20),
      sound_volume: genRandomNumber(10, 100),
      score: genRandomNumber(0, 10 ^ 10),
      type_of_dashboard:
        POSSIBE_DASHBOARD_TYPES[
          Math.floor(Math.random() * POSSIBE_DASHBOARD_TYPES.length)
        ],
      when: genRandomDate().toISOString(),
    }),
    {
      headers: { "Content-Type": "application/json" },
    }
  );
  sleep(0.2);
}
