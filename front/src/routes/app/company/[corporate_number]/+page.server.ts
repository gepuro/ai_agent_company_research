import type { PageServerLoad } from '../$types';
// import { fetchWithJwtServerSide } from '$lib/util/fetchWithJwt'
import { env } from '$env/dynamic/private';
// import type { OrderedHistoryType } from '$lib/type/Ordered';
// import { formatUnixTime } from '$lib/util/formatDate';

async function fetch_company(event) {
  const data = await event.fetch(
    // "http://ai-agent-company-research-backend:3030/api/v1/rag/company?corporate_number=" + event.params.corporate_number,
    env.BACKEND_URL + "/api/v1/rag/company?corporate_number=" + event.params.corporate_number,
  ).then((response) => response.json()).then((data) => {
    return data
  });
  return data;
}

async function fetch_company_name(event) {
  const data = await event.fetch(
    env.BACKEND_URL + "/api/v1/company/houjin_bangou?corporate_number=" + event.params.corporate_number,
  ).then((response) => response.json()).then((data) => {
    return data
  });
  return data;
}

export const load: PageServerLoad = async (event) => {
  // console.log(event.params.corporate_number);

  return {
    // data
    corporate_number: event.params.corporate_number,
    streamed: {
      data: fetch_company(event),
      houjin_bangou: fetch_company_name(event),
    }
  };
};
