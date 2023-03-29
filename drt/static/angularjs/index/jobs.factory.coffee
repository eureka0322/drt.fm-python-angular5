# http://api.pnd.gs/v1/jobs?limit=3&page=1

JobsFactory = (Restangular) ->
  url = 'https://api.pnd.gs/v3/jobs?page=1&limit=3'
  Jobs = {
    loaded: false
    jobs: []
  }

  Jobs.load = ->
    if Jobs.loaded
      return

    Restangular.oneUrl('jobs', url).get().then (response) ->
      Jobs.loaded = true
      Jobs.jobs = []
      for job in response
        job.url = job.title.toString().trim().toLowerCase().replace(/\s+/g, "-").replace(/[^\w\-]+/g, "").replace(/\-\-+/g, "-").replace(/^-+/, "").replace(/-+$/, "")
        Jobs.jobs.push(job)

      return

  return Jobs

angular.module("index.models").factory "JobsFactory", JobsFactory
JobsFactory.$inject = [
  "Restangular"
];