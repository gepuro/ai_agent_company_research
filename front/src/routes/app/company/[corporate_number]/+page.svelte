<script lang="ts">
	import type { PageData } from './$types';
	import { base } from '$app/paths';
	import { onMount } from 'svelte';
	import { fly } from 'svelte/transition';
	import { sineInOut } from 'svelte/easing';
	let loading = true;
	export let data: PageData;
	const corporate_number = data['corporate_number'];
	// メニューの開閉状態を管理する
	let isMenuOpen = false;
	function toggleMenu() {
		isMenuOpen = !isMenuOpen;
	}
	// アニメーション設定
	const transitionProps = {
		duration: 300,
		easing: sineInOut
	};

	type CompanyData = {
		[key: string]: {
			corporate_number?: string;
			name?: { value: string };
			representatives?: { value: string[]; source?: string[] };
			features?: { value: string; source?: string[] };
			phone_number?: { value: string; source?: string[] };
			email?: { value: string; source?: string[] };
			headquarters_location?: { value: string; source?: string[] };
			establishment_year?: { value: string; source?: string[] };
			business_overview?: { value: string; source?: string[] };
			sales?: { [year: string]: { value: string; source?: string[] } };
			employees?: { [year: string]: { value: string; source?: string[] } };
			offices?: { [year: string]: { value: string; source?: string[] } };
			factories?: { [year: string]: { value: string; source?: string[] } };
			stores?: { [year: string]: { value: string; source?: string[] } };
			net_profit?: { [year: string]: { value: string; source?: string[] } };
			capital?: { [year: string]: { value: string; source?: string[] } };
			company_history?: { value: string; source?: string[] };
			philosophy?: { value: string; source?: string[] };
			strengths?: { value: string[]; source?: string[] };
			weaknesses?: { value: string[]; source?: string[] };
			opportunities?: { value: string[]; source?: string[] };
			threats?: { value: string[]; source?: string[] };
			competitors?: { value: string[]; source?: string[] };
			businesses?: { value: string[]; source?: string[] };
			human_resources?: {
				ideal?: { value: string; source?: string[] };
				skills?: { value: string[]; source?: string[] };
			};
		};
	};

	let streamedData: CompanyData;
	let selectedCompany: string | null = null;
	let companyKeys = [];
	let sortedCompanyKeys = [];

	let houjin_bangou = {
		corporate_number: '',
		company_name: '',
		prefecture_name: ''
	};

	// 初期表示設定
	$: if (streamedData && !loading) {
		// 選択中の企業 もしくは、初期選択する企業
		selectedCompany =
			// 法人番号が一致している企業を初期選択にする
			Object.keys(streamedData).find(
				(key) => String(streamedData[key].corporate_number) === String(corporate_number)
			) ||
			// TODO: 法人番号が一致しない場合、企業名が一致する企業を初期選択にする
			Object.keys(streamedData).find(
				(key) => streamedData[key].name?.value === houjin_bangou.company_name
			) ||
			// 法人番号がない企業がある場合は、法人番号がある企業を優先して選択する
			Object.keys(streamedData).find((key) => streamedData[key].corporate_number) ||
			// どちらもない場合は最初の企業を選択する
			Object.keys(streamedData)[0];
	}
	onMount(async () => {
		try {
			streamedData = await data.streamed.data;
			houjin_bangou = await data.streamed.houjin_bangou;

			// console.log('streamedData:', streamedData);

			companyKeys = Object.keys(streamedData);

			// メニュー表示用の企業の配列を生成
			sortedCompanyKeys = companyKeys.sort((a, b) => {
				// 選択された企業を最優先で表示する
				if (a === selectedCompany) return -1;
				if (b === selectedCompany) return 1;

				// 企業名が一致する企業を優先して表示する
				if (streamedData[a].name?.value === houjin_bangou.company_name) return -1;
				if (streamedData[b].name?.value === houjin_bangou.company_name) return 1;

				// 法人番号がある企業を優先して表示する
				if (streamedData[a].corporate_number && !streamedData[b].corporate_number) return -1;
				if (!streamedData[a].corporate_number && streamedData[b].corporate_number) return 1;

				return 0;
			});
			loading = false;
		} catch (error) {
			console.error('Error loading streamed data:', error);
		}
	});

	function selectCompany(companyName) {
		selectedCompany = companyName;
		// メニューを閉じる
		if (isMenuOpen) {
			toggleMenu();
		}
	}
</script>

{#if loading}
	<div class="flex h-screen items-center justify-center">
		<div class="text-center">
			<p class="mb-2 text-lg font-semibold">データを取得しています...</p>
			<p class="text-gray-500">AIが企業データを分析中です...。1〜3分ほど時間がかかります。</p>
			<p class="text-gray-500">
				アクセスが集中すると動作が不安定になることがあります。時間をおいてからご利用ください。
			</p>
			<div class="mt-4 flex justify-center">
				<div class="h-12 w-12 animate-spin rounded-full border-b-2 border-gray-900"></div>
			</div>
		</div>
	</div>
{:else}
	<div class="flex min-h-screen flex-col">
		<!-- ヘッダー -->
		<header class="flex items-center justify-between bg-gray-800 p-4 text-white">
			<h1 class="text-xl font-bold"><a href="/app">3分で企業調査</a></h1>
			<!-- ハンバーガーメニュー -->
			<button
				class="focus:outline-none md:hidden"
				on:click={toggleMenu}
				aria-label="メニューを開閉する"
			>
				{#if isMenuOpen}
					<svg
						xmlns="http://www.w3.org/2000/svg"
						fill="none"
						viewBox="0 0 24 24"
						stroke-width="1.5"
						stroke="currentColor"
						class="h-6 w-6"
					>
						<path stroke-linecap="round" stroke-linejoin="round" d="M6 18L18 6M6 6l12 12" />
					</svg>
				{:else}
					<svg
						xmlns="http://www.w3.org/2000/svg"
						fill="none"
						viewBox="0 0 24 24"
						stroke-width="1.5"
						stroke="currentColor"
						class="h-6 w-6"
					>
						<path
							stroke-linecap="round"
							stroke-linejoin="round"
							d="M3.75 6.75h16.5M3.75 12h16.5m-16.5 5.25h16.5"
						/>
					</svg>
				{/if}
			</button>
		</header>

		<div class="flex flex-1">
			<!-- メニュー -->
			<aside
				class="border-r border-gray-200 bg-gray-100 p-4 md:w-64 {isMenuOpen
					? 'absolute left-0 top-0 z-10 w-full md:w-64'
					: 'hidden md:flex'}"
				transition:fly={{ x: -200, ...transitionProps }}
			>
				<ul class="mt-2 space-y-2">
					<li class="block w-full rounded text-left font-bold">類似企業一覧</li>
					{#each sortedCompanyKeys as companyName}
						<li class:active={selectedCompany === companyName}>
							<button
								class="block w-full rounded p-2 text-left hover:bg-gray-200 focus:bg-gray-200 focus:outline-none"
								on:click={() => selectCompany(companyName)}
							>
								{streamedData[companyName].name?.value || companyName}
							</button>
						</li>
					{/each}
					<li class="block w-full text-left">
						最初に選択した以外の企業について詳細を知りたい場合は、<a
							href="/app"
							class="font-medium text-blue-600 hover:underline dark:text-blue-500">トップページ</a
						>より検索をお願いします。
					</li>
				</ul>
			</aside>

			<!-- コンテンツ -->
			<main class="flex-1 overflow-y-auto p-8">
				{#if selectedCompany && streamedData[selectedCompany]}
					<h1 class="mb-6 text-2xl font-bold">
						{streamedData[selectedCompany].name?.value || selectedCompany}
					</h1>

					<!-- 代表者 -->
					<div class="mb-8">
						<h2 class="mb-2 text-xl font-semibold">
							代表者
							{#if streamedData[selectedCompany].representatives?.source}
								{#each streamedData[selectedCompany].representatives?.source as source}
									<a
										href={source}
										target="_blank"
										rel="noopener noreferrer"
										class="ml-2 text-sm text-blue-500 hover:underline"
									>
										(情報源)
									</a>
								{/each}
							{/if}
						</h2>
						<ul class="list-disc pl-5">
							{#each streamedData[selectedCompany].representatives?.value || [] as representative}
								<li>{representative}</li>
							{/each}
						</ul>
					</div>

					<!-- 特徴 -->
					<div class="mb-8">
						<h2 class="mb-2 text-xl font-semibold">
							特徴
							{#if streamedData[selectedCompany].features?.source}
								{#each streamedData[selectedCompany].features?.source as source}
									<a
										href={source}
										target="_blank"
										rel="noopener noreferrer"
										class="ml-2 text-sm text-blue-500 hover:underline"
									>
										(情報源)
									</a>
								{/each}
							{/if}
						</h2>
						<p>{streamedData[selectedCompany].features?.value}</p>
					</div>
					<!-- 電話番号 -->
					<div class="mb-8">
						<h2 class="mb-2 text-xl font-semibold">
							電話番号
							{#if streamedData[selectedCompany].phone_number?.source}
								{#each streamedData[selectedCompany].phone_number?.source as source}
									<a
										href={source}
										target="_blank"
										rel="noopener noreferrer"
										class="ml-2 text-sm text-blue-500 hover:underline"
									>
										(情報源)
									</a>
								{/each}
							{/if}
						</h2>
						<p>{streamedData[selectedCompany].phone_number?.value}</p>
					</div>
					<!-- メールアドレス -->
					<div class="mb-8">
						<h2 class="mb-2 text-xl font-semibold">
							メールアドレス
							{#if streamedData[selectedCompany].email?.source}
								{#each streamedData[selectedCompany].email?.source as source}
									<a
										href={source}
										target="_blank"
										rel="noopener noreferrer"
										class="ml-2 text-sm text-blue-500 hover:underline"
									>
										(情報源)
									</a>
								{/each}
							{/if}
						</h2>
						<p>{streamedData[selectedCompany].email?.value}</p>
					</div>
					<!-- 本社所在地 -->
					<div class="mb-8">
						<h2 class="mb-2 text-xl font-semibold">
							本社所在地
							{#if streamedData[selectedCompany].headquarters_location?.source}
								{#each streamedData[selectedCompany].headquarters_location?.source as source}
									<a
										href={source}
										target="_blank"
										rel="noopener noreferrer"
										class="ml-2 text-sm text-blue-500 hover:underline"
									>
										(情報源)
									</a>
								{/each}
							{/if}
						</h2>
						<p>{streamedData[selectedCompany].headquarters_location?.value}</p>
					</div>

					<!-- 企業理念 -->
					<div class="mb-8">
						<h2 class="mb-2 text-xl font-semibold">
							企業理念
							{#if streamedData[selectedCompany].philosophy?.source}
								{#each streamedData[selectedCompany].philosophy?.source as source}
									<a
										href={source}
										target="_blank"
										rel="noopener noreferrer"
										class="ml-2 text-sm text-blue-500 hover:underline"
									>
										(情報源)
									</a>
								{/each}
							{/if}
						</h2>
						<p>{streamedData[selectedCompany].philosophy?.value}</p>
					</div>

					<!-- 事業概要 -->
					<div class="mb-8">
						<h2 class="mb-2 text-xl font-semibold">
							事業概要
							{#if streamedData[selectedCompany].business_overview?.source}
								{#each streamedData[selectedCompany].business_overview?.source as source}
									<a
										href={source}
										target="_blank"
										rel="noopener noreferrer"
										class="ml-2 text-sm text-blue-500 hover:underline"
									>
										(情報源)
									</a>
								{/each}
							{/if}
						</h2>
						<p>{streamedData[selectedCompany].business_overview?.value}</p>
					</div>

					<!-- 強み -->
					<div class="mb-8">
						<h2 class="mb-2 text-xl font-semibold">
							強み
							{#if streamedData[selectedCompany].strengths?.source}
								{#each streamedData[selectedCompany].strengths?.source as source}
									<a
										href={source}
										target="_blank"
										rel="noopener noreferrer"
										class="ml-2 text-sm text-blue-500 hover:underline"
									>
										(情報源)
									</a>
								{/each}
							{/if}
						</h2>
						<ul class="list-disc pl-5">
							{#each streamedData[selectedCompany].strengths?.value || [] as strength}
								<li>{strength}</li>
							{/each}
						</ul>
					</div>

					<!-- 弱み -->
					<div class="mb-8">
						<h2 class="mb-2 text-xl font-semibold">
							弱み
							{#if streamedData[selectedCompany].weaknesses?.source}
								{#each streamedData[selectedCompany].weaknesses?.source as source}
									<a
										href={source}
										target="_blank"
										rel="noopener noreferrer"
										class="ml-2 text-sm text-blue-500 hover:underline"
									>
										(情報源)
									</a>
								{/each}
							{/if}
						</h2>
						<ul class="list-disc pl-5">
							{#each streamedData[selectedCompany].weaknesses?.value || [] as weakness}
								<li>{weakness}</li>
							{/each}
						</ul>
					</div>

					<!-- 機会 -->
					<div class="mb-8">
						<h2 class="mb-2 text-xl font-semibold">
							機会
							{#if streamedData[selectedCompany].opportunities?.source}
								{#each streamedData[selectedCompany].opportunities?.source as source}
									<a
										href={source}
										target="_blank"
										rel="noopener noreferrer"
										class="ml-2 text-sm text-blue-500 hover:underline"
									>
										(情報源)
									</a>
								{/each}
							{/if}
						</h2>
						<ul class="list-disc pl-5">
							{#each streamedData[selectedCompany].opportunities?.value || [] as opportunity}
								<li>{opportunity}</li>
							{/each}
						</ul>
					</div>

					<!-- 脅威 -->
					<div class="mb-8">
						<h2 class="mb-2 text-xl font-semibold">
							脅威
							{#if streamedData[selectedCompany].threats?.source}
								{#each streamedData[selectedCompany].threats?.source as source}
									<a
										href={source}
										target="_blank"
										rel="noopener noreferrer"
										class="ml-2 text-sm text-blue-500 hover:underline"
									>
										(情報源)
									</a>
								{/each}
							{/if}
						</h2>
						<ul class="list-disc pl-5">
							{#each streamedData[selectedCompany].threats?.value || [] as threat}
								<li>{threat}</li>
							{/each}
						</ul>
					</div>

					<!-- 競合他社 -->
					<div class="mb-8">
						<h2 class="mb-2 text-xl font-semibold">
							競合他社
							{#if streamedData[selectedCompany].competitors?.source}
								{#each streamedData[selectedCompany].competitors?.source as source}
									<a
										href={source}
										target="_blank"
										rel="noopener noreferrer"
										class="ml-2 text-sm text-blue-500 hover:underline"
									>
										(情報源)
									</a>
								{/each}
							{/if}
						</h2>
						<ul class="list-disc pl-5">
							{#each streamedData[selectedCompany].competitors?.value || [] as competitor}
								<li>{competitor}</li>
							{/each}
						</ul>
					</div>

					<!-- 事業 -->
					<div class="mb-8">
						<h2 class="mb-2 text-xl font-semibold">
							事業
							{#if streamedData[selectedCompany].businesses?.source}
								{#each streamedData[selectedCompany].businesses?.source as source}
									<a
										href={source}
										target="_blank"
										rel="noopener noreferrer"
										class="ml-2 text-sm text-blue-500 hover:underline"
									>
										(情報源)
									</a>
								{/each}
							{/if}
						</h2>
						<ul class="list-disc pl-5">
							{#each streamedData[selectedCompany].businesses?.value || [] as business}
								<li>{business}</li>
							{/each}
						</ul>
					</div>
					<!-- 人材 -->
					<div class="mb-8">
						<h2 class="mb-2 text-xl font-semibold">
							人材
							{#if streamedData[selectedCompany].human_resources?.source}
								{#each streamedData[selectedCompany].human_resources?.source as source}
									<a
										href={source}
										target="_blank"
										rel="noopener noreferrer"
										class="ml-2 text-sm text-blue-500 hover:underline"
									>
										(情報源)
									</a>
								{/each}
							{/if}
						</h2>
						<div class="mb-4">
							<h3 class="font-medium">
								理想の人材像
								{#if streamedData[selectedCompany].human_resources?.ideal?.source}
									{#each streamedData[selectedCompany].human_resources?.ideal?.source as source}
										<a
											href={source}
											target="_blank"
											rel="noopener noreferrer"
											class="ml-2 text-sm text-blue-500 hover:underline"
										>
											(情報源)
										</a>
									{/each}
								{/if}
							</h3>
							<p>{streamedData[selectedCompany].human_resources?.ideal?.value}</p>
						</div>
						<div>
							<h3 class="font-medium">
								必要なスキル
								{#if streamedData[selectedCompany].human_resources?.skills?.source}
									{#each streamedData[selectedCompany].human_resources?.skills?.source as source}
										<a
											href={source}
											target="_blank"
											rel="noopener noreferrer"
											class="ml-2 text-sm text-blue-500 hover:underline"
										>
											(情報源)
										</a>
									{/each}
								{/if}
							</h3>
							<ul class="list-disc pl-5">
								{#each streamedData[selectedCompany].human_resources?.skills?.value || [] as skill}
									<li>{skill}</li>
								{/each}
							</ul>
						</div>
					</div>

					<!-- 会社沿革 -->
					<div class="mb-8">
						<h2 class="mb-2 text-xl font-semibold">
							会社沿革
							{#if streamedData[selectedCompany].company_history?.source}
								{#each streamedData[selectedCompany].company_history?.source as source}
									<a
										href={source}
										target="_blank"
										rel="noopener noreferrer"
										class="ml-2 text-sm text-blue-500 hover:underline"
									>
										(情報源)
									</a>
								{/each}
							{/if}
						</h2>
						<p>{streamedData[selectedCompany].company_history?.value}</p>
					</div>
					<!-- 設立年 -->
					<div class="mb-8">
						<h2 class="mb-2 text-xl font-semibold">
							設立年
							{#if streamedData[selectedCompany].establishment_year?.source}
								{#each streamedData[selectedCompany].establishment_year?.source as source}
									<a
										href={source}
										target="_blank"
										rel="noopener noreferrer"
										class="ml-2 text-sm text-blue-500 hover:underline"
									>
										(情報源)
									</a>
								{/each}
							{/if}
						</h2>
						<p>{streamedData[selectedCompany].establishment_year?.value}</p>
					</div>

					<!-- 売上 -->
					<div class="mb-8">
						<h2 class="mb-2 text-xl font-semibold">売上</h2>
						{#if streamedData[selectedCompany].sales}
							<ul>
								{#each Object.entries(streamedData[selectedCompany].sales) as [year, saleData]}
									<li class="mb-2">
										<span class="font-medium">{year}</span>: <span>{saleData.value}</span>
										{#if saleData.source}
											{#each saleData.source as source}
												<a
													href={source}
													target="_blank"
													rel="noopener noreferrer"
													class="ml-2 text-sm text-blue-500 hover:underline">(情報源)</a
												>
											{/each}
										{/if}
									</li>
								{/each}
							</ul>
						{/if}
					</div>

					<!-- 従業員数 -->
					<div class="mb-8">
						<h2 class="mb-2 text-xl font-semibold">従業員数</h2>
						{#if streamedData[selectedCompany].employees}
							<ul>
								{#each Object.entries(streamedData[selectedCompany].employees) as [year, employeeData]}
									<li class="mb-2">
										<span class="font-medium">{year}</span>: <span>{employeeData.value}</span>
										{#if employeeData.source}
											{#each employeeData.source as source}
												<a
													href={source}
													target="_blank"
													rel="noopener noreferrer"
													class="ml-2 text-sm text-blue-500 hover:underline">(情報源)</a
												>
											{/each}
										{/if}
									</li>
								{/each}
							</ul>
						{/if}
					</div>

					<!-- 営業利益 -->
					<div class="mb-8">
						<h2 class="mb-2 text-xl font-semibold">営業利益</h2>
						{#if streamedData[selectedCompany].net_profit}
							<ul>
								{#each Object.entries(streamedData[selectedCompany].net_profit) as [year, profitData]}
									<li class="mb-2">
										<span class="font-medium">{year}</span>: <span>{profitData.value}</span>
										{#if profitData.source}
											{#each profitData.source as source}
												<a
													href={source}
													target="_blank"
													rel="noopener noreferrer"
													class="ml-2 text-sm text-blue-500 hover:underline">(情報源)</a
												>
											{/each}
										{/if}
									</li>
								{/each}
							</ul>
						{/if}
					</div>

					<!-- 資本金 -->
					<div class="mb-8">
						<h2 class="mb-2 text-xl font-semibold">資本金</h2>
						{#if streamedData[selectedCompany].capital}
							<ul>
								{#each Object.entries(streamedData[selectedCompany].capital) as [year, capitalData]}
									<li class="mb-2">
										<span class="font-medium">{year}</span>: <span>{capitalData.value}</span>
										{#if capitalData.source}
											{#each capitalData.source as source}
												<a
													href={source}
													target="_blank"
													rel="noopener noreferrer"
													class="ml-2 text-sm text-blue-500 hover:underline">(情報源)</a
												>
											{/each}
										{/if}
									</li>
								{/each}
							</ul>
						{/if}
					</div>

					<!-- オフィス -->
					<!-- <div class="mb-8">
						<h2 class="mb-2 text-xl font-semibold">オフィス</h2>
						{#if streamedData[selectedCompany].offices}
							<ul>
								{#each Object.entries(streamedData[selectedCompany].offices) as [year, officeData]}
									<li class="mb-2">
										<span class="font-medium">{year}</span>: <span>{officeData.value}</span>
										{#if officeData.source}
											{#each officeData.source as source}
												<a
													href={source}
													target="_blank"
													rel="noopener noreferrer"
													class="ml-2 text-sm text-blue-500 hover:underline">(情報源)</a
												>
											{/each}
										{/if}
									</li>
								{/each}
							</ul>
						{/if}
					</div> -->

					<!-- 工場 -->
					<!-- <div class="mb-8">
						<h2 class="mb-2 text-xl font-semibold">工場</h2>
						{#if streamedData[selectedCompany].factories}
							<ul>
								{#each Object.entries(streamedData[selectedCompany].factories) as [year, factoryData]}
									<li class="mb-2">
										<span class="font-medium">{year}</span>: <span>{factoryData.value}</span>
										{#if factoryData.source}
											{#each factoryData.source as source}
												<a
													href={source}
													target="_blank"
													rel="noopener noreferrer"
													class="ml-2 text-sm text-blue-500 hover:underline">(情報源)</a
												>
											{/each}
										{/if}
									</li>
								{/each}
							</ul>
						{/if}
					</div> -->

					<!-- 店舗 -->
					<!-- <div class="mb-8">
						<h2 class="mb-2 text-xl font-semibold">店舗</h2>
						{#if streamedData[selectedCompany].stores}
							<ul>
								{#each Object.entries(streamedData[selectedCompany].stores) as [year, storeData]}
									<li class="mb-2">
										<span class="font-medium">{year}</span>: <span>{storeData.value}</span>
										{#if storeData.source}
											{#each storeData.source as source}
												<a
													href={source}
													target="_blank"
													rel="noopener noreferrer"
													class="ml-2 text-sm text-blue-500 hover:underline">(情報源)</a
												>
											{/each}
										{/if}
									</li>
								{/each}
							</ul>
						{/if}
					</div> -->

					<!-- 法人番号 -->
					<div class="mb-8">
						<h2 class="mb-2 text-xl font-semibold">法人番号</h2>
						<p>{streamedData[selectedCompany].corporate_number}</p>
					</div>
				{:else}
					<p>企業を選択してください。</p>
				{/if}
			</main>
		</div>
	</div>
	<!-- フッター -->
	<footer class="bg-gray-800 p-2 text-center text-white">
		<p>
			データの正確性を上げるために最善の努力をしていますが、情報の正確性を保証するものではありません。<a
				href="https://docs.google.com/forms/d/e/1FAIpQLSca4JuiA9Z_0FvBCJqALWM3H8sm0H524zIZYPkQpMF0WE1x8w/viewform"
				class="underline">データの不備は、こちらからご連絡をお願いします。</a
			>
		</p>
	</footer>
{/if}

<style>
	.active button {
		background-color: #ddd;
	}
</style>
