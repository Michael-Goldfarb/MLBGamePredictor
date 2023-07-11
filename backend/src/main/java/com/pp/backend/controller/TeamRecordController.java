package com.pp.backend.controller;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;
import java.util.List;
import com.pp.backend.entity.TeamRecord;
import com.pp.backend.service.TeamRecordService;

@RestController
@RequestMapping("/api/team-records")
public class TeamRecordController {
    private final TeamRecordService teamRecordService;

    public TeamRecordController(TeamRecordService teamRecordService) {
        this.teamRecordService = teamRecordService;
    }

    @GetMapping
    public ResponseEntity<List<TeamRecord>> getTeamRecords() {
        List<TeamRecord> teamRecords = teamRecordService.getTeamRecords();
        return ResponseEntity.ok(teamRecords);
    }
}
