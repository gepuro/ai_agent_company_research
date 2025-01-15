import type { PageServerLoad } from '../$types';
import { env } from '$env/dynamic/private';

async function fetch_recent_generated_companies(event) {
    const data = await event.fetch(
        env.BACKEND_URL + "/api/v1/company/cache",
    ).then((response) => response.json()).then((data) => {
        return data
    });
    return data;
}

export const load: PageServerLoad = async (event) => {
    return {
        streamed: {
            recent_generated_companies: fetch_recent_generated_companies(event),
        }
    };
};
