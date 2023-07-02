--Covid 19 Data Exploration 

--Skills used: Joins, CTE's, Temp Tables, Windows Functions, Aggregate Functions, Creating Views, Converting Data Types


--Selecting the Data that we are using
select location, date,total_cases,new_cases,total_deaths,population
from ProjectCovid..CovidDeaths$
order by 1,2


--Looking at the Total Cases and Total Deaths
--Shows likelyhood of death via contracting covid in your country
select location, date,total_cases,total_deaths, (total_deaths/total_cases)*100 as Death_Percentage
from ProjectCovid..CovidDeaths$
Where location like '%states%'
order by 1,2


--Looking at cases vs population
--Shows the percentage of the population that got covid
select location, date,population,total_cases,total_deaths, (total_cases/population)*100 as Population_Percentage
from ProjectCovid..CovidDeaths$
Where location like '%states%'
order by 1,2


--Countries with highest Infection rates compared to population
SELECT  location, population, MAX(total_cases) as HighestInfectionCount, (MAX(total_cases)/population)*100 as Population_Percentage
FROM ProjectCovid..CovidDeaths$
-- Where location like '%states%'
GROUP BY 
  location, population
ORDER BY 
  Population_Percentage DESC;


-- Showing Countries with Highest Death Count per Population
SELECT Location, MAX(CAST(Total_Deaths AS INT)) AS TotalDeathCount
FROM ProjectCovid..CovidDeaths$
--Where location like '%states%'
Where continent is not null 
GROUP BY location
ORDER BY TotalDeathCount DESC;


-- BREAKING THINGS DOWN BY CONTINENT
-- Showing contintents with the highest death count per population
Select continent, MAX(cast(Total_deaths as int)) as TotalDeathCount
From ProjectCovid..CovidDeaths$
--Where location like '%states%'
Where continent is not null 
Group by continent
order by TotalDeathCount desc


-- GLOBAL NUMBERS
Select SUM(new_cases) as total_cases, SUM(cast(new_deaths as int)) as total_deaths, SUM(cast(new_deaths as int))/SUM(New_Cases)*100 as DeathPercentage
From ProjectCovid..CovidDeaths$
--Where location like '%states%'
where continent is not null 
--Group By date
order by 1,2


-- Total Population vs Vaccinations
-- Shows Percentage of Population that has recieved at least one Covid Vaccine
SELECT dea.continent, dea.location, dea.date, dea.population, vac.new_vaccinations
, SUM(CONVERT(int,vac.new_vaccinations)) OVER (PARTITION BY dea.Location ORDER BY dea.location, dea.Date) AS RollingPeopleVaccinated
(RollingPeopleVaccinated/population)*100
FROM ProjectCovid..CovidDeaths$ dea
JOIN ProjectCovid..CovidVaccinations$ vac
	ON dea.location = vac.location
	AND dea.date = vac.date
WHERE dea.continent IS NOT NULL 
ORDER BY 2,3


-- Using CTE to perform Calculation on Partition By in previous query

WITH PopvsVac (Continent, Location, Date, Population, New_Vaccinations, RollingPeopleVaccinated) AS 
(
SELECT dea.continent, dea.location, dea.date, dea.population, vac.new_vaccinations
, SUM(CONVERT(int,vac.new_vaccinations)) OVER (PARTITION BY dea.Location ORDER BY dea.location, dea.Date) AS RollingPeopleVaccinated
--, (RollingPeopleVaccinated/population)*100
FROM ProjectCovid..CovidDeaths$ dea
JOIN ProjectCovid..CovidVaccinations$ vac
	ON dea.location = vac.location
	AND dea.date = vac.date
WHERE dea.continent IS NOT NULL 
--order by 2,3
)
SELECT *, (RollingPeopleVaccinated/Population)*100 AS Percentage_of_People_Vaccinated
FROM PopvsVac


-- Using Temp Table to perform Calculation on Partition By in previous query

DROP Table if exists #PercentPopulationVaccinated
Create Table #PercentPopulationVaccinated
(
Continent nvarchar(255),
Location nvarchar(255),
Date datetime,
Population numeric,
New_vaccinations numeric,
RollingPeopleVaccinated numeric
)

Insert into #PercentPopulationVaccinated
Select dea.continent, dea.location, dea.date, dea.population, vac.new_vaccinations
, SUM(CONVERT(bigint,ISNULL(vac.new_vaccinations, 0))) OVER (Partition by dea.Location Order by dea.location, dea.Date) as RollingPeopleVaccinated
From ProjectCovid..CovidDeaths$ dea
Join ProjectCovid..CovidVaccinations$ vac
	On dea.location = vac.location
	and dea.date = vac.date
where dea.population is not null and dea.population != 0 

Select *, (RollingPeopleVaccinated/Population)*100 AS Percentage_of_People_Vaccinated
From #PercentPopulationVaccinated


-- Creating View to store data for later visualizations

Create View PercentPopulationVaccinated as
Select dea.continent, dea.location, dea.date, dea.population, vac.new_vaccinations
, SUM(CONVERT(int,vac.new_vaccinations)) OVER (Partition by dea.Location Order by dea.location, dea.Date) as RollingPeopleVaccinated
--, (RollingPeopleVaccinated/population)*100
From ProjectCovid..CovidDeaths$ dea
Join ProjectCovid..CovidVaccinations$ vac
	On dea.location = vac.location
	and dea.date = vac.date
where dea.continent is not null 
