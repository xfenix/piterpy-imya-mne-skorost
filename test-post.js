import http from "k6/http";
import { sleep } from "k6";
import { Faker } from "@faker-js/faker";

const POSSIBE_DASHBOARD_TYPES = [1, 2, 3];
const fakerObj = new Faker();
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
      user_name: fakerObj.person.firstName(),
      sound_volume: fakerObj.rangeToNumber({ min: 10, max: 100 }),
      score: fakerObj.rangeToNumber({ min: 0, max: 10 ^ 10 }),
      type_of_dashboard:
        POSSIBE_DASHBOARD_TYPES[
          Math.floor(Math.random() * POSSIBE_DASHBOARD_TYPES.length)
        ],
      when: fakerObj.date.recent().toISOString(),
    }),
    {
      headers: { "Content-Type": "application/json" },
    }
  );
  sleep(0.2);
}
