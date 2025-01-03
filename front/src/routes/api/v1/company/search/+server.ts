import { env } from '$env/dynamic/private';
// import { env } from '$env/static/private';


export const GET = async (event) => {
  // URLパラメータ company_name を取得
  const url = event.request.url;
  const params = new URL(url).searchParams;
  const company_name = params.get('company_name')
  if (!company_name) {
    return { status: 400, body: 'company_name is required' };
  }
  const encodedCompanyName = encodeURIComponent(company_name);
  const data = await event.fetch(
    env.BACKEND_URL + `/api/v1/company/search?company_name=${encodedCompanyName}`,
  ).then((response) => response.json()).then((data) => {
    return data
  });
  const response = new Response(JSON.stringify(data), {
    headers: { 'Content-Type': 'application/json' }
  });
  return response;
};