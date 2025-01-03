<script lang="ts">
	let searchTerm = '';
	let searchResults: Company[] = [];
	let selectedCompany: Company | null = null;
	let isLoading = false;
	let error: Error | null = null;
	let debounceTimer;

	interface Company {
		company_name: string;
		address: string;
		corporate_number: string;
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
		window.location.href = `/company/${company.corporate_number}`;
	}
</script>

<div class="flex min-h-screen flex-col items-center justify-start bg-gray-100">
	<div class="mt-10 w-full max-w-md">
		<div class="relative">
			<h1 class="mb-4 text-2xl font-bold">3分で企業研究</h1>
			<input
				type="text"
				class="w-full rounded border p-3 focus:border-blue-500 focus:outline-none focus:ring"
				placeholder="企業名を入力"
				bind:value={searchTerm}
				on:input={handleInputChange}
			/>
			{#if isLoading}
				<div class="absolute left-0 top-12 w-full rounded border bg-white p-4 shadow-md">
					<p class="text-gray-600">検索中...</p>
				</div>
			{/if}
			{#if error}
				<div class="absolute left-0 top-12 w-full rounded border bg-white p-4 shadow-md">
					<p class="text-red-600">エラーが発生しました: {error.message}</p>
				</div>
			{/if}
			{#if searchResults.length > 0 && searchTerm.length >= 3}
				<ul class="absolute left-0 top-12 w-full rounded border bg-white shadow-md">
					{#each searchResults as company}
						<li
							class="cursor-pointer p-2 hover:bg-gray-100"
							on:click={() => selectCompany(company)}
						>
							<p class="font-medium">{company.company_name}</p>
							<p class="text-sm text-gray-600">{company.concatenation_address}</p>
						</li>
					{/each}
				</ul>
			{/if}
		</div>

		<!-- {#if selectedCompany}
			<div class="mt-4 rounded border bg-white p-4 shadow-md">
				<h2 class="mb-2 text-lg font-bold">選択された企業</h2>
				<p><strong>企業名:</strong> {selectedCompany.company_name}</p>
				<p><strong>住所:</strong> {selectedCompany.concatenation_address}</p>
			</div>
		{/if} -->
	</div>
</div>
