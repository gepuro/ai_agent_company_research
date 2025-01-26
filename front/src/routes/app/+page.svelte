<script lang="ts">
	import { onMount } from 'svelte';
	let searchTerm = '';
	let searchResults: Company[] = [];
	let selectedCompany: Company | null = null;
	let isLoading = false;
	let error: Error | null = null;
	let debounceTimer;
	export let data: PageData;

	onMount(() => {
		document.title = '3分で企業調査 | PittariData';
	});

	interface Company {
		company_name: string;
		address: string;
		corporate_number: string;
		concatenation_address: string;
	}

	const searchCompanies = async () => {
		if (!searchTerm.trim() || searchTerm.length < 3) {
			searchResults = [];
			return;
		}

		isLoading = true;
		error = null;

		try {
			const encodedSearchTerm = encodeURIComponent(searchTerm);
			const response = await fetch(`/api/v1/company/search?company_name=${encodedSearchTerm}`);

			if (!response.ok) {
				throw new Error(`HTTP error! status: ${response.status}`);
			}

			const data = await response.json();
			searchResults = data;
		} catch (err) {
			error = err as Error;
			searchResults = [];
		} finally {
			isLoading = false;
		}
	};

	const handleInputChange = () => {
		clearTimeout(debounceTimer);
		debounceTimer = setTimeout(() => {
			searchCompanies();
		}, 300);
	};

	function selectCompany(company: Company) {
		// ページ遷移処理
		window.location.href = `/app/company/${company.corporate_number}`;
	}
</script>

<div class="flex min-h-screen flex-col items-center justify-start bg-gray-50">
	<div class="mt-12 w-full max-w-md px-4">
		<div class="relative mb-4">
			<h1 class="text-2xl font-bold text-gray-900">3分で企業調査</h1>
		</div>
	</div>
	<div class="z-10 mt-4 w-full max-w-md px-4">
		<div class="relative">
			<div class="relative">
				<input
					type="text"
					class="w-full rounded-md border border-gray-300 bg-white py-3 pl-12 pr-4 text-gray-700 placeholder-gray-400 focus:border-blue-500 focus:outline-none focus:ring focus:ring-blue-200"
					placeholder="企業名を入力"
					bind:value={searchTerm}
					on:input={handleInputChange}
				/>
				<div class="pointer-events-none absolute inset-y-0 left-0 flex items-center pl-3">
					<svg
						xmlns="http://www.w3.org/2000/svg"
						fill="none"
						viewBox="0 0 24 24"
						stroke-width="1.5"
						stroke="currentColor"
						class="h-5 w-5 text-gray-400"
					>
						<path
							stroke-linecap="round"
							stroke-linejoin="round"
							d="M21 21l-5.197-5.197m0 0A7.5 7.5 0 105.196 5.196a7.5 7.5 0 0010.607 10.607z"
						/>
					</svg>
				</div>
			</div>

			{#if isLoading}
				<div
					class="absolute left-0 top-16 w-full rounded-md border border-gray-200 bg-white p-4 shadow-md"
				>
					<div class="flex items-center">
						<div class="mr-3 h-5 w-5 animate-spin rounded-full border-b-2 border-gray-900"></div>
						<p class="text-gray-600">検索中...</p>
					</div>
				</div>
			{/if}
			{#if error}
				<div
					class="absolute left-0 top-16 w-full rounded-md border border-red-200 bg-white p-4 shadow-md"
				>
					<p class="font-medium text-red-600">エラーが発生しました: {error.message}</p>
				</div>
			{/if}
			{#if searchResults.length > 0 && searchTerm.length >= 3}
				<ul
					class="absolute left-0 top-16 w-full rounded-md border border-gray-200 bg-white shadow-md"
				>
					{#each searchResults as company}
						<li
							class="cursor-pointer p-3 hover:bg-gray-100"
							on:click={() => selectCompany(company)}
						>
							<p class="font-medium text-gray-800">{company.company_name}</p>
							<p class="text-sm text-gray-500">{company.concatenation_address}</p>
						</li>
					{/each}
				</ul>
			{/if}
		</div>
	</div>
	<div class="mt-8 w-full max-w-md px-4">
		<div>
			スマートフォンからの利用は動作が不安定なようです。パソコンからのアクセスをお願いします。また、「最近に調査された企業」が表示されない場合はアクセスが集中しています。時間をおいてからのご利用をお願いします。
		</div>
	</div>
	{#await data.streamed.recent_generated_companies then recent_generated_companies}
		<div class="mt-8 w-full max-w-md px-4">
			<h2 class="mb-4 text-lg font-semibold text-gray-900">最近に調査された企業</h2>
			<ul>
				{#each recent_generated_companies as company}
					<li class="p-1">
						<a
							href="/app/company/{company.corporate_number}"
							class="font-medium text-blue-600 transition-colors duration-200 hover:text-blue-700 hover:underline"
						>
							{company.company_name}
						</a>
					</li>
				{/each}
			</ul>
		</div>
	{/await}
	<div class="mt-10"></div>
	<div class="border-gray-3w00 z-0 mt-auto w-full border-t p-4 text-center">
		<ul class="flex flex-col justify-center sm:flex-row">
			<li class="mb-2 mr-8">
				<a
					href="https://gepuro.net"
					class="font-medium text-blue-600 hover:underline dark:text-blue-500"
					>開発者のプロフィール</a
				>
			</li>
			<li class="mb-2">
				<a
					href="https://docs.google.com/forms/d/e/1FAIpQLSca4JuiA9Z_0FvBCJqALWM3H8sm0H524zIZYPkQpMF0WE1x8w/viewform?usp=dialog"
					class="font-medium text-blue-600 hover:underline dark:text-blue-500"
				>
					アンケートへのご協力をお願いします。🙇
				</a>
			</li>
		</ul>
	</div>
</div>
